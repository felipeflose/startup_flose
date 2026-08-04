from flose.solutions.floseup_199_po_evil_boss_refatorar_src_flo_2cba6b import *

def test_po_evil_boss_refatorar_sr_success():
    """
    Testa se a função po_evil_boss_refatorar_sr realiza a refatoração esperada.
    """
    # Simulação da chamada da função com o cenário esperado
    result = po_evil_boss_refatorar_sr()
    
    # Verificação do resultado esperado (baseado na simulação do bloco anterior)
    expected_result = "👔 Felipe: ${duel.active_hero} class=\"hsl(280, 70%, 60%)\""
    
    assert result == expected_result, f"A refatoração falhou. Esperado: {expected_result}, Obtido: {result}"

def test_po_evil_boss_refatorar_sr_no_style():
    """
    Testa o caso onde o estilo inline não é encontrado.
    """
    result = po_evil_boss_refatorar_sr()
    
    assert "Refatoração não aplicada ou estilo não encontrado" in result