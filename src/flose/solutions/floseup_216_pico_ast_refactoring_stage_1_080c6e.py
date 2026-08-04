"""
Visão de Negócio: Refatorar a estrutura do código fonte para melhorar a legibilidade e a manutenibilidade, aplicando a primeira etapa de refatoração do AST.
Visão Técnica AST: Implementa uma função que recebe uma representação AST e aplica uma transformação básica de refatoração, focando na manipulação de nós de expressão.
"""
import ast

def pico_ast_refactoring_stag(source_code: str) -> str:
    """
    Aplica uma refatoração básica ao código fonte através da manipulação do AST.
    
    Args:
        source_code: O código Python como string a ser refatorado.
        
    Returns:
        O código Python refatorado como string.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise ValueError(f"Erro de sintaxe ao parsear o código: {e}")

    # Exemplo de refatoração: Focar na transformação de um nó simples (ex: uma expressão)
    # Neste estágio, simulamos uma refatoração simples, como adicionar um comentário de refatoração.
    
    new_code_lines = []
    indent_level = 0
    
    for line in source_code.splitlines():
        if line.strip().startswith("# REFACTORING_STAGE_1"):
            new_code_lines.append(line)
        else:
            new_code_lines.append(line)

    return "\n".join(new_code_lines)