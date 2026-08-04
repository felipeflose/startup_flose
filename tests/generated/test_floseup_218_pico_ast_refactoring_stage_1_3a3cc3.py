from flose.solutions.floseup_218_pico_ast_refactoring_stage_1_3a3cc3 import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código de exemplo.
    """
    sample_code = """
def pico_function(x):
    if x > 10:
        return x * 2
    return x
"""
    expected_output = """def refactored_pico_function(x):
    if x > 10:
        return x * 2
    return x"""

    result = pico_ast_refactoring_stag(sample_code)
    
    assert result == expected_output