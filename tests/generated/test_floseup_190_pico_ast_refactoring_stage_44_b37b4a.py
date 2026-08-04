# tests/test_floseup_190_pico_ast_refactoring_stage_44_b37b4a.py

from flose.solutions.floseup_190_pico_ast_refactoring_stage_44_b37b4a import refactor_code

def test_refactor_code():
    code = """
def old_function():
    print("Hello, World!")
"""
    expected_output = """
@deprecated
def old_function():
    print("Hello, World!")
"""
    assert refactor_code(code) == expected_output