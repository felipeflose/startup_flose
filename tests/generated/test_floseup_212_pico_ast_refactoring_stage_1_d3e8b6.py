from flose.solutions.floseup_212_pico_ast_refactoring_stage_1_d3e8b6 import *

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código fonte simples.
    """
    source_code = """
def calculate_sum(a, b):
    result = a + b
    return result
"""
    
    result = pico_ast_refactoring_stag(source_code)
    
    # Verificação básica para garantir que a função foi processada e o AST foi analisado
    assert isinstance(result, str)
    assert "# Refatorado: calculate_sum" in result
    assert "ASSIGNMENT_SIMPLIFIED" in result
    assert "def calculate_sum(a, b):" in result