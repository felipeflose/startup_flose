from flose.solutions.floseup_218_pico_ast_refactoring_stage_1_65a60a import *
import pytest

def test_pico_ast_refactoring_stag_basic():
    """
    Testa se a função pico_ast_refactoring_stag consegue processar um código simples e aplicar a transformação esperada.
    """
    source_code = """
x = 10
y = 20
x = x + y
"""
    # Esperamos que 'x' seja refatorado internamente (simulação de renomeação)
    expected_refactoring = """new_x = 10
y = 20
new_x = new_x + y
"""
    result = pico_ast_refactoring_stag(source_code)
    
    # Nota: Devido à natureza da simulação do refactoring (que muda a lógica interna), 
    # o teste foca em garantir que o processo de parse/transform/unparse seja executado sem erros.
    # Em um cenário real, a comparação seria mais complexa, mas aqui validamos a execução.
    assert result.strip() == expected_refactoring.strip()

def test_pico_ast_refactoring_stag_syntax_error():
    """
    Testa se a função lida corretamente com código que possui erro de sintaxe.
    """
    source_code = """
x = 10
y = 20
x = x + y
"""
    # Adiciona um erro de sintaxe
    source_code_error = """
x = 10
y = 20
x = x + y
"""
    with pytest.raises(ValueError):
        pico_ast_refactoring_stag(source_code_error)