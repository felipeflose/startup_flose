from flose.solutions.floseup_198_pico_ast_refactoring_stage_1_53b3fa import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código de exemplo.
    """
    sample_code = """
def calculate_total(items):
    total_amount = 0
    for item in items:
        total_amount += item.price
    return total_amount
"""
    
    # Executa a refatoração
    refactored_code = pico_ast_refactoring_stag(sample_code)
    
    # Verifica se o código foi alterado e se a estrutura AST foi processada
    assert refactored_code != sample_code
    
    # Verifica se o código refatorado ainda é sintaticamente válido
    try:
        ast.parse(refactored_code)
    except SyntaxError:
        pytest.fail("O código refatorado não é sintaticamente válido.")

    # Verifica se as variáveis foram renomeadas (verificação simplificada)
    assert "refactored_total_amount" in refactored_code
    assert "refactored_items" in refactored_code