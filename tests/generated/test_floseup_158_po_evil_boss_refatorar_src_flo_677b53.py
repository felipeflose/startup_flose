from flose.solutions.floseup_158_po_evil_boss_refatorar_src_flo_677b53 import *

def test_po_evil_boss_refatorar_sr():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que a refatoração do estilo inline
    para classes CSS baseadas em HSL seja aplicada corretamente.
    """
    # Simulação do objeto necessário para o teste
    class MockDuel:
        def __init__(self, reason):
            self.active_card = type('Card', (object,), {'po_rejection_reason': reason})()

    # Teste 1: Caso onde a razão de rejeição existe
    mock_duel_present = MockDuel("Reason exists for testing.")
    result_present = po_evil_boss_refatorar_sr.__globals__['po_evil_boss_refatorar_sr'](mock_duel_present)
    
    expected_present = '<div class="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 Reason exists for testing.</div>'

    assert result_present == expected_present, "Teste falhou para o caso com razão de rejeição presente."

    # Teste 2: Caso onde a razão de rejeição é nula (empty)
    mock_duel_empty = MockDuel("")
    result_empty = po_evil_boss_refatorar_sr.__globals__['po_evil_boss_refatorar_sr'](mock_duel_empty)
    
    expected_empty = ''

    assert result_empty == expected_empty, "Teste falhou para o caso com razão de rejeição vazia."

    print("Todos os testes para po_evil_boss_refatorar_sr foram aprovados.")