from flose.solutions.floseup_204_pico_ast_refactoring_stage_1_d9c018 import optimize_code

def test_optimize_code():
    # Test case 1: Loop with a single pass statement should be removed
    input_code = """
for i in range(5):
    pass
"""
    expected_output = ""
    assert optimize_code(input_code) == expected_output

    # Test case 2: Assignment to constant can be simplified
    input_code = "x = 4 + 3"
    expected_output = "x = 7"
    assert optimize_code(input_code) == expected_output

    # Test case 3: Binary addition of constants should be combined
    input_code = "(1 + 2) + (3 + 4)"
    expected_output = "7"
    assert optimize_code(input_code) == expected_output

    # Test case 4: If statement with a constant condition should be simplified
    input_code = """
if True:
    print('Hello')
else:
    print('World')
"""
    expected_output = "print('Hello')"
    assert optimize_code(input_code) == expected_output

    # Test case 5: Complex expression with multiple optimizations
    input_code = "(1 + 2) * (3 - 4) + 5"
    expected_output = "-3"
    assert optimize_code(input_code) == expected_output