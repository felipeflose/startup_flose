import os
import ast
import random
import subprocess
import re
from typing import Optional, Tuple

def update_branch(repo_path: str):
    """Garante que o auditor esteja olhando para o código mais recente do Git."""
    try:
        print("[PO Auditor] 📥 Sincronizando com a branch remota para pegar o código mais novo...")
        # Atualiza a branch (ignora erros silenciosamente caso não haja upstream configurado)
        subprocess.run(
            ["git", "pull", "--rebase"], 
            cwd=repo_path, 
            capture_output=True,
            timeout=100
        )
    except Exception as e:
        print(f"[PO Auditor] Aviso: Falha ao atualizar a branch: {e}")

class BaseCodeSmellVisitor(ast.NodeVisitor):
    def __init__(self, filename: str, code_lines: list):
        self.filename = filename
        self.code_lines = code_lines
        self.smells = []

    def add_smell(self, type_: str, node: ast.AST, msg: str):
        line = getattr(node, 'lineno', 1)
        snippet = self.code_lines[line - 1].strip() if 0 <= line - 1 < len(self.code_lines) else ""
        self.smells.append((self.filename, type_, line, msg, snippet))

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # 1. Documentação técnica
        if not ast.get_docstring(node):
            self.add_smell("Backend/Docstring", node, f"A função '{node.name}' no módulo '{self.filename}' não possui docstring.")
        
        # 2. Type hint no retorno
        if node.returns is None:
            self.add_smell("Backend/Typing", node, f"A função '{node.name}' não possui anotação de tipo no retorno (ex: -> Dict[str, Any]).")

        # 3. Complexidade / Tamanho da Função
        end_lineno = getattr(node, 'end_lineno', node.lineno)
        length = end_lineno - node.lineno
        if length > 40:
            self.add_smell("Backend/Refatoracao", node, f"A função '{node.name}' possui {length} linhas. Aplicar refatoração Clean Code!")

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if not ast.get_docstring(node):
            self.add_smell("Backend/AsyncDocstring", node, f"Função async '{node.name}' está sem documentação técnica.")
            
        if node.returns is None:
            self.add_smell("Backend/AsyncTyping", node, f"Função async '{node.name}' não possui anotação de tipo de retorno.")

        end_lineno = getattr(node, 'end_lineno', node.lineno)
        length = end_lineno - node.lineno
        if length > 40:
            self.add_smell("Backend/AsyncPerformance", node, f"Corotina assíncrona '{node.name}' com {length} linhas. Módulo deve ser modularizado!")
            
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None or (isinstance(node.type, ast.Name) and node.type.id == "Exception"):
            self.add_smell("Backend/TratamentoErros", node, "Exceção ampla (except Exception). Especificar exceção explícita ou tratar com logger.")
        self.generic_visit(node)

def scan_frontend_smells(filename: str, code: str) -> list:
    """Procura falhas no código Frontend (HTML, JS, CSS)."""
    smells = []
    lines = code.splitlines()
    for idx, line in enumerate(lines, 1):
        if "console.log(" in line:
            smells.append((filename, "Frontend/JS", idx, "Vazamento de logs de debug (console.log) em código de produção.", line.strip()))
        if "style=" in line and len(line) > 100:
            smells.append((filename, "Frontend/CSS", idx, "Estilo inline extenso. Extraia para CSS modular com classes HSL.", line.strip()))
        if "setInterval(" in line:
            smells.append((filename, "Frontend/Performance", idx, "Uso de setInterval detectado. Prefira requestAnimationFrame ou EventBus.", line.strip()))
    return smells

def scan_host_codebase(src_dir: str = "src/flose") -> Optional[Tuple[str, str]]:
    """
    Escaneia o repositório REAL via AST em busca de falhas de código.
    Retorna uma tupla (topic_title, topic_desc) baseada no código real.
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(src_dir)))
    update_branch(repo_root)

    all_smells = []
    
    for root, dirs, files in os.walk(src_dir):
        # 🚫 Ignorar a pasta 'solutions' (onde ficam os módulos gerados pelos Heróis)
        dirs[:] = [d for d in dirs if d != "solutions"]
        if "solutions" in root.split(os.sep):
            continue

        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, repo_root)
            if file.endswith(".py"):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        code = f.read()
                        lines = code.splitlines()
                        
                    tree = ast.parse(code, filename=filepath)
                    visitor = BaseCodeSmellVisitor(rel_path, lines)
                    visitor.visit(tree)
                    all_smells.extend(visitor.smells)

                    fe_smells = scan_frontend_smells(rel_path, code)
                    all_smells.extend(fe_smells)

                except Exception as e:
                    print(f"[PO Auditor] Falha ao analisar AST de {file}: {e}")

    if not all_smells:
        return None
        
    chosen = random.choice(all_smells)
    filename, smell_type, line_num, msg, snippet = chosen
    
    title = f"Refatorar {filename}: {smell_type} (Linha {line_num})"
    desc = (
        f"PO Vilão realizou auditoria AST no código REAL do repositório host:\n\n"
        f"- **Arquivo Real**: `{filename}`\n"
        f"- **Linha Afetada**: L{line_num}\n"
        f"- **Código Atual**: `{snippet}`\n"
        f"- **Diagnóstico AST**: {msg}\n\n"
        f"⚠️ **Exigência do PO Vilão:** Corrigir este trecho de código no repositório com implementação Python REAL e testes Pytest!"
    )
           
    return title, desc
