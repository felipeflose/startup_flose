from flose.solutions.floseup_235_pico_ast_refactoring_stage_1_61e7b1 import *

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código Python válido.
    """
    test_code = """
def calculate(a, b):
    result = a + b
    print(result)
    return result

x = 10
y = 5
z = calculate(x, y)
"""
    
    # Esperamos que a função retorne o código AST unparsed (refatorado)
    refactored = pico_ast_refactoring_stag(test_code)
    
    # Verificação básica para garantir que o processo não falhou e gerou um output
    assert isinstance(refactored, str)
    assert len(refactored) > 0
    
    # Verificação de conteúdo (opcional, mas útil para refatoração)
    assert "def calculate(a, b):" in refactored
    assert "return result" in refactored