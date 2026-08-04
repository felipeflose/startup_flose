from flose.solutions.floseup_206_pico_ast_refactoring_stage_1_a2f91a import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código Python simples.
    """
    test_code = """
def calculate(a, b):
    result = a + b
    return result

x = 10
"""
    
    # Esperamos que a função retorne uma string que represente o código refatorado
    result = pico_ast_refactoring_stag(test_code)
    
    # Verificação básica para garantir que a execução não falhou e que o resultado é uma string
    assert isinstance(result, str)
    assert "Refactored function definition" in result
    assert "def calculate(a, b):" in result
    assert "x = 10" in result

def test_pico_ast_refactoring_stag_syntax_error():
    """
    Testa o tratamento de erro quando o código de entrada possui um erro de sintaxe.
    """
    invalid_code = "def func(a, b: int"  # Sintaxe inválida
    result = pico_ast_refactoring_stag(invalid_code)
    
    # Esperamos que a função retorne uma mensagem de erro, conforme implementado
    assert "Error parsing source code" in result