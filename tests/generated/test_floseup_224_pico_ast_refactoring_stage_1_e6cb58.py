import pytest
from flose.solutions.floseup_224_pico_ast_refactoring_stage_1_e6cb58 import optimize_python_code

def test_optimize_python_code():
    code = """
    while True:
        if condition:
            break
    """
    optimized_code = optimize_python_code(code)
    assert 'if' not in optimized_code.co_code.decode()

    code = """
    for i in range(10):
        pass
    """
    optimized_code = optimize_python_code(code)
    assert 'for' not in optimized_code.co_code.decode()