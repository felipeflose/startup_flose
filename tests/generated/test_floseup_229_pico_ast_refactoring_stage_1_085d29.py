from flose.solutions.floseup_229_pico_ast_refactoring_stage_1_085d29 import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código simples.
    """
    source = """
def calculate(a, b):
    result = a + b
    return result
"""
    expected_start = "def calculate(a, b):\n    ast.Expr(value=ast.Constant(value=\"--- Refatorado ---\"))\n    result = a + b\n    return result"
    
    result = pico_ast_refactoring_stag(source)
    
    assert "--- Refatorado ---" in result
    assert "def calculate(a, b):" in result
    assert "result = a + b" in result
    assert "return result" in result