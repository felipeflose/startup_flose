from flose.solutions.floseup_202_pico_ast_refactoring_stage_1_e7a401 import pico_ast_refactoring_stag

def test_pico_ast_refactoring_stag():
    """Testa a função pico_ast_refactoring_stag com um código de exemplo."""
    # Código de entrada que contém a variável a ser refatorada
    input_code = """
def original_var_name(x):
    original_var_name = x * 2
    return original_var_name
"""

    expected_output = """
def refactored_var_name(x):
    refactored_var_name = x * 2
    return refactored_var_name
"""

    # Executa a função
    actual_output = pico_ast_refactoring_stag(input_code)

    # Verifica o resultado
    assert actual_output.strip() == expected_output.strip()
    print("Teste de refatoração AST aprovado.")