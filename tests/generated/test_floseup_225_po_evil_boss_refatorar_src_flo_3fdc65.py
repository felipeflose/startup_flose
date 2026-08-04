import pytest
from flose.solutions.floseup_225_po_evil_boss_refatorar_src_flo_3fdc65 import po_evil_boss_refatorar_sr

def test_refactor_style_extraction():
    # Cenário 1: Rejeição existe (caminho com conteúdo)
    duel_data_with_rejection = {
        'active_card': {
            'po_rejection_reason': "Rejeição por motivo XXXXX"
        }
    }
    expected_output_with_rejection = '<div class="style-po-rejection-reason font-size-sm color-error-5555 mb-sm">💬 Rejeição por motivo XXXXX</div>'
    
    result_with_rejection = po_evil_boss_refatorar_sr(duel_data_with_rejection)
    assert expected_output_with_rejection == result_with_rejection

    # Cenário 2: Rejeição não existe (caminho vazio)
    duel_data_no_rejection = {
        'active_card': {
            'po_rejection_reason': None
        }
    }
    expected_output_no_rejection = ''
    
    result_no_rejection = po_evil_boss_refatorar_sr(duel_data_no_rejection)
    assert expected_output_no_rejection == result_no_rejection