from flose.solutions.floseup_210_pico_ast_refactoring_stage_1_93ab49 import optimize_ast

def test_optimize_ast():
    code = """
def add(a, b):
    return a + 0

def greet():
    print("Hello", end=" ")

def foo(x):
    return x
"""
    optimized_code, stats = optimize_ast(code)
    
    expected_code = """
def add(a, b):
    return a

def greet():
    print("Hello")

def foo(x):
    x
"""
    assert ast.unparse(optimized_code) == expected_code
    
    # Verificar estatísticas de otimizações
    expected_stats = {
        'BinOp': 2,
        'Call': 1,
        'FunctionDef': 3
    }
    assert stats == expected_stats

def test_optimize_ast_no_changes():
    code = """
def add(a, b):
    return a + b

def greet(name):
    print("Hello", name)

def multiply(x, y):
    return x * y
"""
    optimized_code, stats = optimize_ast(code)
    
    assert ast.unparse(optimized_code) == ast.unparse(ast.parse(code))
    
    # Verificar estatísticas de otimizações
    expected_stats = {
        'BinOp': 0,
        'Call': 1,
        'FunctionDef': 3
    }
    assert stats == expected_stats

def test_optimize_ast_with_complex_code():
    code = """
def calculate_discount(price, discount):
    return price * (1 - discount)

def get_user_age(user_data):
    if user_data['age'] is not None:
        return user_data['age']
    else:
        return 0
"""
    optimized_code, stats = optimize_ast(code)
    
    expected_code = """
def calculate_discount(price, discount):
    return price * (1 - discount)

def get_user_age(user_data):
    if user_data['age'] is not None:
        return user_data['age']
    else:
        return 0
"""
    assert ast.unparse(optimized_code) == expected_code
    
    # Verificar estatísticas de otimizações
    expected_stats = {
        'BinOp': 1,
        'Call': 1,
        'FunctionDef': 2
    }
    assert stats == expected_stats