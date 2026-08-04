"""
Visão de Negócio: Este script tem como objetivo garantir a conformidade das funções assíncronas no módulo `po_auditor.py` com as diretrizes de documentação PEP 257.

Visão Técnica AST: O script utiliza o módulo `ast` para varrer e inspecionar todas as definições de funções assíncronas em um módulo Python, verificando a presença e formato da docstring.
"""

import ast
from flose.solutions.floseup_223_po_evil_boss_refatorar_src_flo_f95a7b import refactor_async_function_docs

# Função auxiliar para carregar o conteúdo de um módulo como uma AST
def load_module_as_ast(module_path):
    with open(module_path, 'r') as file:
        return ast.parse(file.read())

# Função auxiliar para salvar a AST em um arquivo
def save_ast_to_file(ast_node, output_path):
    with open(output_path, 'w') as file:
        file.write(ast.unparse(ast_node))

# Caminho do módulo original e caminho de saída para o módulo refatorado
original_module_path = "src/flose/agents/po_auditor.py"
output_module_path = "src/flose/agents/refactored_po_auditor.py"

# Carrega a AST do módulo original
module_ast = load_module_as_ast(original_module_path)

# Refatora as docstrings das funções assíncronas
refactor_async_function_docs(module_ast)

# Salva a AST refatorada em um novo arquivo
save_ast_to_file(module_ast, output_module_path)