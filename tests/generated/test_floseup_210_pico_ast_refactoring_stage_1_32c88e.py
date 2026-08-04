import pytest
import ast

# Importação obrigatória conforme regra 4a
from flose.solutions.floseup_210_pico_ast_refactoring_stage_1_32c88e import pico_ast_refactoring_stag

def test_pico_ast_refactoring_stag_renames_variables():
    """
    Testa se a função pico_ast_refactoring_stag consegue renomear corretamente
    as variáveis na AST do código de entrada.
    """
    source_code = """
x = 10
y = x + 5
result = y * 2
"""
    prefix = "refactored_"
    
    # Executa a função a ser testada
    refactored_code = pico_ast_refactoring_stag(source_code, prefix)
    
    # Espera o resultado refatorado
    expected_code = """
x = refactored_x
y = refactored_x + 5
result = refactored_y * 2
"""
    
    # Verifica se o código refatorado corresponde ao esperado
    assert refactored_code.strip() == expected_code.strip()

def test_pico_ast_refactoring_stag_handles_complex_names():
    """
    Testa a refatoração com nomes de variáveis mais complexos.
    """
    source_code = """
total_score = 100
final_value = total_score * 2
"""
    prefix = "renamed_"
    
    refactored_code = pico_ast_refactoring_stag(source_code, prefix)
    
    expected_code = """
total_score = renamed_total_score
final_value = renamed_total_score * 2
"""
    
    assert refactored_code.strip() == expected_code.strip()