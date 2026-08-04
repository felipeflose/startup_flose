from flose.solutions.floseup_226_pico_ast_refactoring_stage_1_5389b0 import pico_ast_refactoring_stag

import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa se a função pico_ast_refactoring_stag processa o código e retorna uma string válida.
    """
    input_code = "def func(x): return x + 1\nprint(func(5))"
    
    result = pico_ast_refactoring_stag(input_code)
    
    # Verifica se o resultado contém a marcação de refatoração
    assert "# --- Refactoring Stage 1 Applied ---" in result
    
    # Verifica se o código original está presente
    assert input_code in result
    
    # Verifica se o resultado é uma string
    assert isinstance(result, str)

def test_pico_ast_refactoring_stag_syntax_error():
    """
    Testa o tratamento de erro quando o código de entrada tem erro de sintaxe.
    """
    invalid_code = "def func(x): return" # Código inválido
    
    result = pico_ast_refactoring_stag(invalid_code)
    
    # Verifica se a mensagem de erro esperada foi retornada
    assert "Erro de sintaxe ao analisar o código" in result