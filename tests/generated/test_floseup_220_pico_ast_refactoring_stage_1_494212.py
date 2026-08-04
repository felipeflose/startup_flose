from flose.solutions.floseup_220_pico_ast_refactoring_stage_1_494212 import *
import pytest
import ast

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código de exemplo.
    """
    source = """
def calculate_sum(a, b):
    result = a + b
    return result

def process_data(data):
    if data > 10:
        print("Data is large")
    else:
        print("Data is small")
"""
    expected_refactoring = """
def calculate_sum(a, b):
    result = a + b
    return result

def process_data(data):
    if data > 10:
        print("Data is large")
    else:
        print("Data is small")
"""
    result = pico_ast_refactoring_stag(source)
    
    # Como a função simplesmente reestrutura o AST e o unparse,
    # o teste verifica se a saída é uma representação válida do código.
    assert result.strip() == expected_refactoring.strip()

def test_pico_ast_refactoring_stag_empty():
    """
    Testa a função com código vazio.
    """
    source = ""
    result = pico_ast_refactoring_stag(source)
    assert result == ""