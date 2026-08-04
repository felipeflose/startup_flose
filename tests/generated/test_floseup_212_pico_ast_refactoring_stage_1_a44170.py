from flose.solutions.floseup_212_pico_ast_refactoring_stage_1_a44170 import optimize_code

def test_optimize_code():
    # Test case 1: Simplify multiplication by zero
    original_code = "result = 5 * 0"
    expected_code = "result = 0"
    assert optimize_code(original_code) == expected_code
    
    # Test case 2: Remove unnecessary arguments from print calls
    original_code = "print('Hello', None)"
    expected_code = "print('Hello')"
    assert optimize_code(original_code) == expected_code
    
    # Test case 3: Complex example with multiple optimizations
    original_code = """
def calculate(x):
    if x > 0:
        result = 1 + 2 * 0
    else:
        result = None
    return result
"""
    expected_code = """
def calculate(x):
    if x > 0:
        result = 3
    else:
        result = None
    return result
"""
    assert optimize_code(original_code) == expected_code

# Run the tests
test_optimize_code()
print("All tests passed!")