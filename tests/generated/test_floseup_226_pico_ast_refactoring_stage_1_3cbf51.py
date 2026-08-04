from flose.solutions.floseup_226_pico_ast_refactoring_stage_1_3cbf51 import * # Assuming this is the module name

def test_optimize_code():
    code = """
def calculate(a, b, c):
    x = a + b
    y = b * c
    z = x + y
    return z

result = calculate(10, 20, 30)
print(result)
"""
    optimized_code = optimize_code(code)
    exec(optimized_code)
    
    # Expected to print 70
    assert result == 70

def test_variable_optimization():
    code = """
def multiply(a, b):
    x = a * b
    y = a + b
    z = x * y
    return z

result = multiply(2, 3)
print(result)
"""
    optimized_code = optimize_code(code)
    exec(optimized_code)
    
    # Expected to print 48 (since the function call can be optimized away)
    assert result == 15

def test_function_call_optimization():
    code = """
def add(a, b):
    return a + b

def calculate(x, y):
    z = x * y
    w = add(z, x)
    return w

result = calculate(2, 3)
print(result)
"""
    optimized_code = optimize_code(code)
    exec(optimized_code)
    
    # Expected to print 8 (since the function call can be replaced with a simple variable reference)
    assert result == 10