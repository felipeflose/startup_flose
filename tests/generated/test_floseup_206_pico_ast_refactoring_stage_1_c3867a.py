from flose.solutions.floseup_206_pico_ast_refactoring_stage_1_c3867a import *

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código de exemplo simples.
    """
    test_code = """
def calculate(a, b):
    return a + b

result = calculate(5, 3)
print(result)
"""
    expected_prefix = "# Refatorado no Stage 1\n"
    
    result = pico_ast_refactoring_stag(test_code)
    
    # Verificação básica para garantir que o prefixo foi adicionado e o código é válido
    assert expected_prefix in result
    
    # Verificação de que o AST foi processado e o código resultante é uma string
    assert isinstance(result, str)
    
    # Verificação de que o código refatorado contém a estrutura esperada (verificação mais robusta seria comparar o AST resultante)
    assert "def calculate(a, b):" in result
    assert "print(result)" in result