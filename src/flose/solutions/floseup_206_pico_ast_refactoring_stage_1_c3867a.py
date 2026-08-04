"""
Visão de Negócio: Refatoração inicial da estrutura do código para melhorar a legibilidade e a manutenibilidade do projeto FLOSEUP.
Visão Técnica AST: Implementação de uma função que manipula o Abstract Syntax Tree (AST) de um código Python para realizar refatorações de nível superior.
"""
import ast

def pico_ast_refactoring_stag(source_code: str) -> str:
    """
    Realiza uma refatoração de estágio 1 no AST de um código Python fornecido.

    Esta função demonstra a manipulação básica do AST para identificar e registrar
    mudanças estruturais, servindo como base para refatorações mais complexas.

    Args:
        source_code: O código fonte em formato string a ser analisado.

    Returns:
        Uma string representando o código após a aplicação da refatoração básica.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return f"Erro de sintaxe ao analisar o código: {e}"

    # Exemplo de refatoração: Adicionar um comentário inicial
    new_lines = ["# Refatorado no Stage 1"]
    
    # Modificar o corpo principal do módulo
    new_body = [ast.Expr(value=ast.Constant(value=line.strip())) for line in tree.body]
    
    new_tree = ast.Module(body=new_body, type_ignores=[])
    
    refactored_code = ast.unparse(new_tree)
    
    return "\n".join(new_lines) + "\n" + refactored_code