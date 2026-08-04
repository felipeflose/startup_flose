"""
Visão de Negócio: Refatorar a estrutura do código Python para melhorar a legibilidade e a manutenção do código-fonte interno.
Visão Técnica AST: Implementar uma função que percorre uma Árvore de Sintaxe Abstrata (AST) de uma expressão simples e renomeia todas as variáveis encontradas para um prefixo específico.
"""
import ast

class AstRefactorer(ast.NodeTransformer):
    """
    Transformer que renomeia nomes de variáveis em um nó AST.
    """
    def __init__(self, prefix: str):
        self.prefix = prefix

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            node.id = f"{self.prefix}_{node.id}"
        return self.visit(node)

def pico_ast_refactoring_stag(source_code: str, prefix: str) -> str:
    """
    Refatora o código-fonte fornecido aplicando renomeação de variáveis via AST.

    Args:
        source_code: O código Python como string a ser analisado.
        prefix: O prefixo a ser adicionado aos nomes das variáveis.

    Returns:
        O código Python refatorado como string.
    """
    tree = ast.parse(source_code)
    refactorer = AstRefactorer(prefix)
    new_tree = refactorer.visit(tree)
    ast.fix_missing_locations(new_tree)
    return ast.unparse(new_tree)

if __name__ == '__main__':
    test_code = """
x = 10
y = x + 5
result = y * 2
"""
    refactored_code = pico_ast_refactoring_stag(test_code, "refactored_")
    print(refactored_code)