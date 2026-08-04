# tests/test_refactor_code.py

import pytest
from flose.solutions.floseup_192_pico_ast_refactoring_stage_44_97c2be import refactor_code, simplify_loops, optimize_variable_names

def test_refactor_code():
    original_code = "print('Hello, World!')"
    expected_code = "logging.info('Hello, World!')"
    assert refactor_code(original_code) == expected_code

def test_simplify_loops():
    code = """
for i in range(10):
    print(i)
"""
    simplified_code = """
for index in range(10):
    logging.info(index)
"""
    assert simplify_loops(code) == simplified_code

def test_optimize_variable_names():
    code = "for i in range(10): print(i)"
    optimized_code = "for item_index in range(10): logging.info(item_index)"
    assert optimize_variable_names(code) == optimized_code