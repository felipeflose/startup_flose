from flose.solutions.floseup_235_pico_ast_refactoring_stage_1_7d2fbe import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_success():
    """
    Testa a função pico_ast_refactoring_stag com um código Python válido.
    """
    test_code = """
def calculate_sum(a, b):
    result = a + b
    return result

x = 10
print(x)
"""
    expected_output_start = "def calculate_sum(a, b):\n    --- Refatorado Stage 1 ---\n    result = a + b\n    return result\nx = 10\nprint(x)"

    result = pico_ast_refactoring_stag(test_code)

    # Verificação básica para garantir que a função foi chamada e o resultado é uma string
    assert isinstance(result, str)
    
    # Verificação da presença da refatoração dentro da função
    assert "--- Refatorado Stage 1 ---" in result
    
    # Verificação de que o código foi processado (comparação parcial)
    assert expected_output_start in result
    
    # Teste de erro de sintaxe
    error_code = "def invalid_syntax("
    result_error = pico_ast_refactoring_stag(error_code)
    assert "Erro de sintaxe" in result_error