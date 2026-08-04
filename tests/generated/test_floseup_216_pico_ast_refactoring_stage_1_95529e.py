from flose.solutions.floseup_216_pico_ast_refactoring_stage_1_95529e import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código Python simples.
    """
    source_code = """
def long_function_name():
    x = 1
    y = 2
    return x + y
"""
    expected_output = """def refactored_long_function_name():
    x = 1
    y = 2
    return x + y"""
    
    result = pico_ast_refactoring_stag(source_code)
    
    assert result == expected_output

def test_pico_ast_refactoring_stag_syntax_error():
    """
    Testa o tratamento de erro quando o código de entrada possui erro de sintaxe.
    """
    source_code = "def function():\n    if True: print()" # Sintaxe inválida
    
    result = pico_ast_refactoring_stag(source_code)
    
    assert "Erro de sintaxe ao analisar o código" in result