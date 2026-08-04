from flose.solutions.floseup_200_pico_ast_refactoring_stage_1_b35345 import *
import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa se a função pico_ast_refactoring_stag consegue parsear e manipular o AST de forma básica.
    """
    source = "def func(a):\n    b = a + 1\n    return b"
    expected_output = "def refactored_function(a):\n    b = a + 1\n    return b"
    
    result = pico_ast_refactoring_stag(source)
    
    assert result == expected_output
    
    # Testar caso vazio ou malformado (garantindo robustez)
    with pytest.raises(SyntaxError):
        pico_ast_refactoring_stag("def incomplete(")