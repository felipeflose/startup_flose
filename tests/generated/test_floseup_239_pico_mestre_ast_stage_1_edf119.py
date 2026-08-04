from flose.solutions.floseup_239_pico_mestre_ast_stage_1_edf119 import pico_mestre_ast_stage_1

def test_pico_mestre_ast_stage_1_basic():
    """
    Testa a função pico_mestre_ast_stage_1 com um código simples.
    """
    source_code = "a = 10\nb = 5\nresult = a + b"
    expected_output_start = "# Optimized: a = 10"
    
    result = pico_mestre_ast_stage_1(source_code)
    
    # Verificação básica para garantir que a função foi chamada e retornou algo
    assert isinstance(result, str)
    assert expected_output_start in result
    assert "Optimized:" in result
    
    # Teste de caso de erro (opcional, mas bom para robustez)
    invalid_code = "def func(x): return"
    result_error = pico_mestre_ast_stage_1(invalid_code)
    assert "Erro de sintaxe" in result_error