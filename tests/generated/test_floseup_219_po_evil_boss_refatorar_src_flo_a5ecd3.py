from flose.solutions.floseup_219_po_evil_boss_refatorar_src_flo_a5ecd3 import *

def test_po_evil_boss_refatorar_sr():
    """
    Verifica se a função po_evil_boss_refatorar_sr refatora corretamente o estilo inline para classes CSS.
    """
    # Simulação da execução da função com o código de exemplo fornecido no card
    expected_output = (
        "${duel.active_card.po_rejection_reason ? '<div class=\"po-rejection-reason-box\">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>' : ''}"
    )
    
    actual_output = po_evil_boss_refatorar_sr()
    
    assert actual_output == expected_output, "A refatoração do estilo inline para classes CSS falhou."

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr()