from flose.solutions.floseup_235_pico_ast_refactoring_stage_1_75376b import *
import pytest

def test_pico_ast_refactoring_stag_basic_refactoring():
    """
    Testa a função pico_ast_refactoring_stag com um código fonte simples.
    """
    original_code = """
def calculate_sum(a, b):
    old_result = a + b
    return old_result
"""
    expected_refactored_code = """
def calculate_sum(a, b):
    new_result = a + b
    return new_result
"""
    refactored = pico_ast_refactoring_stag(original_code)
    assert refactored == expected_refactored_code

def test_pico_ast_refactoring_stag_syntax_error():
    """
    Testa o tratamento de erro para código fonte com erro de sintaxe.
    """
    invalid_code = "def func(a, b"
    result = pico_ast_refactoring_stag(invalid_code)
    assert "Erro de sintaxe" in result