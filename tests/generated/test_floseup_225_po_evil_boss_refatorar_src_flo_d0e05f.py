from flose.solutions.floseup_225_po_evil_boss_refatorar_src_flo_d0e05f import *

def test_po_evil_boss_refatorar_sr():
    # Setup de dados simulados para o teste
    class MockCard:
        def __init__(self, reason):
            self.po_rejection_reason = reason

    duel = MockCard("Reason for rejection simulation")

    # Execução da função refatorada
    result = po_evil_boss_refatorar_sr(duel)

    # Verificação esperada (assumindo que as classes foram aplicadas corretamente)
    expected_output = '<div class="po-rejection-reason-text po-rejection-reason-color po-rejection-reason-margin">💬 Reason for rejection simulation</div>'

    assert result == expected_output
    assert "po-rejection-reason-text" in result
    assert "po-rejection-reason-color" in result
    assert "po-rejection-reason-margin" in result
    assert "💬 Reason for rejection simulation" in result