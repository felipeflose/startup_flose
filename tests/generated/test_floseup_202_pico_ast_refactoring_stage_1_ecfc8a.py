from flose.solutions.floseup_202_pico_ast_refactoring_stage_1_ecfc8a import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic_refactoring():
    """
    Testa a função pico_ast_refactoring_stag com um código simples para garantir a funcionalidade básica.
    """
    original_code = """
a = 10 + 5
b = 20 - 3
result = a + b
print(result)
"""
    expected_output = """
a = 15
b = 17
result = 32
print(result)
"""
    refactored_code = pico_ast_refactoring_stag(original_code)

    # A verificação deve ser feita comparando o resultado refatorado com o esperado.
    # Nota: Devido à natureza da refatoração AST, a formatação exata pode variar ligeiramente,
    # mas a lógica da transformação deve ser mantida.
    assert refactored_code.strip() == expected_output.strip()

def test_pico_ast_refactoring_stag_syntax_error():
    """
    Testa a função com código que contém um erro de sintaxe para verificar o tratamento de exceções.
    """
    invalid_code = "a = 10 + "
    with pytest.raises(ValueError):
        pico_ast_refactoring_stag(invalid_code)