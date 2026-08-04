from flose.solutions.floseup_158_po_evil_boss_refatorar_src_flo_5bf60c import *

def test_po_evil_boss_refatorar_sr():
    # Teste de caso 1: Quando a razão de rejeição existe
    po_rejection_reason_present = "Reason for rejection example"
    expected_output_present = "po-rejection-reason-style po-rejection-reason-color💬 Reason for rejection example"
    
    result_present = po_evil_boss_refatorar_sr(po_rejection_reason_present)
    assert result_present == expected_output_present, "Teste falhou para caso com razão de rejeição presente"

    # Teste de caso 2: Quando a razão de rejeição é vazia (False)
    po_rejection_reason_empty = None
    expected_output_empty = ""
    
    result_empty = po_evil_boss_refatorar_sr(po_rejection_reason_empty)
    assert result_empty == expected_output_empty, "Teste falhou para caso com razão de rejeição vazia"

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr()