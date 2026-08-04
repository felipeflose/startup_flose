import pytest
from flose.solutions.floseup_219_po_evil_boss_refatorar_src_flo_f36f0e import *

def test_refactoring_functionality():
    # Simulação do código original (L1346)
    original_code = (
        "${duel.active_card.po_rejection_reason ? "
        "<div style=\"font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;\">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>"
        ": ''}"
    )
    
    # Executar a função de refatoração
    refactored_code = po_evil_boss_refatorar_sr(original_code)
    
    # Esperar o resultado refatorado
    expected_refactored = (
        '<div class="po-evil-boss-style">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>'
    )
    
    # Verificar se a refatoração ocorreu conforme o esperado
    assert refactored_code == expected_refactored