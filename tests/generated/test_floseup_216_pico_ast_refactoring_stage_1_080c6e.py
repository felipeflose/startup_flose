from flose.solutions.floseup_216_pico_ast_refactoring_stage_1_080c6e import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa se a função pico_ast_refactoring_stag consegue processar e retornar o código.
    """
    test_input = "def my_function(x):\n    return x + 1"
    
    # Esperamos que a função retorne o código com o marcador de refatoração aplicado
    expected_output = "def my_function(x):\n    return x + 1\n# REFACTORING_STAGE_1"
    
    result = pico_ast_refactoring_stag(test_input)
    
    assert result == expected_output
    
    # Testar com um código mais longo
    test_input_2 = """
def calculate(a, b):
    result = a + b
    return result
"""
    expected_output_2 = """
def calculate(a, b):
    result = a + b
    return result
# REFACTORING_STAGE_1
"""
    result_2 = pico_ast_refactoring_stag(test_input_2)
    assert result_2 == expected_output_2