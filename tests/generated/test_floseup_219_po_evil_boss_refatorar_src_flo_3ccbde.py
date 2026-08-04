from flose.solutions.floseup_219_po_evil_boss_refatorar_src_flo_3ccbde import *

def test_po_evil_boss_refatorar_sr():
    # Teste de caso 1: Conteúdo presente
    input_content_1 = "${duel.active_card.po_rejection_reason.substring(0, 50)}"
    expected_output_1 = f'<div class="po_rejection_reason_style">💬 {input_content_1}</div>'
    
    result_1 = po_evil_boss_refatorar_sr(input_content_1)
    assert result_1 == expected_output_1, "Teste 1 falhou: A refatoração do estilo inline não resultou nas classes CSS corretas."

    # Teste de caso 2: Conteúdo vazio (caso de fallback)
    input_content_2 = ""
    expected_output_2 = ""
    
    result_2 = po_evil_boss_refatorar_sr(input_content_2)
    assert result_2 == expected_output_2, "Teste 2 falhou: O tratamento de conteúdo vazio não foi correto."

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr()