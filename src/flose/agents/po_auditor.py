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
    def __init__(self, filename: str):
        self.filename = filename
        self.smells = []

    def add_smell(self, type_: str, node: ast.AST, msg: str):
        line = getattr(node, 'lineno', '?')
        self.smells.append((self.filename, type_, line, msg))

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if not ast.get_docstring(node):
            self.add_smell("Backend/Docstring", node, f"A função '{node.name}' não possui documentação técnica.")
        
        end_lineno = getattr(node, 'end_lineno', node.lineno)
        length = end_lineno - node.lineno
        if length > 50:
            self.add_smell("Backend/Complexidade", node, f"A função '{node.name}' é um monstro de {length} linhas. Dividir responsabilidades!")
            
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if not ast.get_docstring(node):
            self.add_smell("Backend/Docstring", node, f"Endpoint/Task assíncrona '{node.name}' está sem documentação.")
            
        end_lineno = getattr(node, 'end_lineno', node.lineno)
        length = end_lineno - node.lineno
        if length > 50:
            self.add_smell("Backend/Complexidade", node, f"Endpoint '{node.name}' possui {length} linhas. Aplicar Clean Architecture!")
            
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None or (isinstance(node.type, ast.Name) and node.type.id == "Exception"):
            self.add_smell("Backend/TratamentoErros", node, "Tratamento de exceção genérico (except Exception). Oculte falhas silenciosas!")
        self.generic_visit(node)

def scan_frontend_smells(filename: str, code: str) -> list:
    """Procura falhas no código Frontend (HTML, JS, CSS)."""
    smells = []
    if "console.log(" in code:
        smells.append((filename, "Frontend/JS", "?", "Vazamento de logs de debug (console.log) em código de produção."))
    if "style=" in code:
        smells.append((filename, "Frontend/CSS", "?", "Uso excessivo de estilos inline (style=...). Extraia para classes CSS isoladas!"))
    if "setInterval(" in code:
        smells.append((filename, "Frontend/Performance", "?", "Uso de setInterval detectado. Pode causar memory leak, prefira requestAnimationFrame ou WebSockets."))
    return smells

def scan_host_codebase(src_dir: str = "src/flose") -> Optional[Tuple[str, str]]:
    """
    Atualiza o repositório, escaneia arquivos em busca de "Code Smells" Fullstack.
    Retorna uma tupla (topic_title, topic_desc) pronta para o Jira.
    """
    # Descobre a raiz do repositório a partir do src_dir
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(src_dir)))
    update_branch(repo_root)

    all_smells = []
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith(".py"):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        code = f.read()
                        
                    tree = ast.parse(code, filename=filepath)
                    visitor = BaseCodeSmellVisitor(file)
                    visitor.visit(tree)
                    all_smells.extend(visitor.smells)

                    # Além da AST Backend, varre por HTML/JS embutidos (ex: em web_app.py)
                    fe_smells = scan_frontend_smells(file, code)
                    all_smells.extend(fe_smells)

                except Exception as e:
                    print(f"[PO Auditor] Falha ao parear {file}: {e}")

    if not all_smells:
        return None
        
    # Sorteia um dos problemas encontrados para delegar ao time
    chosen = random.choice(all_smells)
    filename, smell_type, line_num, msg = chosen
    
    title = f"Refatorar {filename}: Corrigir {smell_type}"
    desc = f"PO Vilão escaneou o repositório REAL e achou uma falha arquitetural:\n\n" \
           f"- **Arquivo**: `{filename}`\n" \
           f"- **Linha**: {line_num}\n" \
           f"- **Problema**: {msg}\n\n" \
           f"Heróis, corrijam isso urgentemente antes que o sistema caia!"
           
    return title, desc
