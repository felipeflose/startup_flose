from flose.solutions.floseup_225_po_evil_boss_refatorar_src_flo_d45ac7 import *

def test_po_evil_boss_refatorar_sr():
    # Cenário de teste com o código original (simulação)
    original_code = (
        "${duel.active_card.po_rejection_reason ? '<div style=\"font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;\">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>' : ''}"
    )

    # Executar a refatoração
    refactored_code = po_evil_boss_refatorar_sr(original_code)

    # Verificação esperada (A refatoração deve substituir o style inline pela classe)
    expected_class = 'class="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;"'
    
    # A refatoração deve ter substituído o atributo style pelo class
    assert expected_class in refactored_code
    assert 'style=' not in refactored_code
    assert 'class=' in refactored_code
    assert refactored_code.startswith(f'<div {expected_class}')
    
    print("Teste de refatoração AST concluído com sucesso.")

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr()