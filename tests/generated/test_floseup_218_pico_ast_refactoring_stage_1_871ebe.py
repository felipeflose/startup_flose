import pytest
import ast
from flose.solutions.floseup_218_pico_ast_refactoring_stage_1_871ebe import pico_ast_refactoring_stag

def test_pico_ast_refactoring_stag_basic():
    """Testa a função pico_ast_refactoring_stag com um código simples."""
    source_code = "x = 1 + 2\ny = x * 3"
    
    # Esperamos que a função refatore a expressão de soma
    refactored_code = pico_ast_refactoring_stag(source_code)
    
    # Verifica se a refatoração ocorreu (simulação de verificação)
    assert "x = 3" in refactored_code
    assert "y = x" in refactored_code

def test_pico_ast_refactoring_stag_syntax_error():
    """Testa a função com código que causa erro de sintaxe."""
    with pytest.raises(ValueError):
        pico_ast_refactoring_stag("x = 1 +")