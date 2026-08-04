from flose.solutions.floseup_211_po_evil_boss_refatorar_src_flo_58115f import *

async def test_po_evil_boss_refatorar_sr():
    # Testando a refatoração da assinatura
    # Assumindo que a função refatorada agora é assíncrona e retorna None
    result = await po_evil_boss_refatorar_sr()
    assert result is None
    
    # Verificação de que a função existe e é assíncrona (implícito pela regra)
    assert callable(po_evil_boss_refatorar_sr)