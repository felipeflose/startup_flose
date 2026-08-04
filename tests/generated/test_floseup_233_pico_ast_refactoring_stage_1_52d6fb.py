from flose.solutions.floseup_233_pico_ast_refactoring_stage_1_52d6fb import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa a função pico_ast_refactoring_stag com um código de exemplo simples.
    """
    original_code = """
def calculate_sum(a, b):
    result = a + b
    return result

x = 10
y = 20
final = calculate_sum(x, y)
"""
    
    # Esperamos que a função seja renomeada ao ser processada pelo refactoring
    refactored_code = pico_ast_refactoring_stag(original_code)
    
    # Verificamos se o código foi alterado (exemplo: verificar se as funções foram renomeadas)
    assert "refactored_calculate_sum" in refactored_code
    assert "final = refactored_calculate_sum(x, y)" in refactored_code
    
    # Teste de caso de erro de sintaxe
    error_code = "def invalid_syntax("
    result_error = pico_ast_refactoring_stag(error_code)
    assert "Erro de Sintaxe" in result_error