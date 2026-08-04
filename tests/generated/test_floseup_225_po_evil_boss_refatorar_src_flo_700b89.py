from flose.solutions.floseup_225_po_evil_boss_refatorar_src_flo_700b89 import *

def test_po_evil_boss_refatorar_sr():
    """Testa a refatoração do trecho de código de estilo inline para classes CSS."""
    
    # Simulação da execução da função refatorar
    result = po_evil_boss_refatorar_sr()

    # Esperado: O resultado deve conter classes CSS em vez de estilos inline.
    # O resultado refatorado deve seguir o padrão de classes geradas.
    expected_pattern = '<div class="po-rejection-reason--0.38rem po-rejection-reason--#ff5555 po-rejection-reason--0.2rem">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>'

    # Verifica se o resultado refatorado contém a estrutura de classe esperada.
    assert expected_pattern in result, "O código refatorado não contém as classes CSS esperadas."

    # Verifica se o conteúdo do texto foi preservado.
    assert "💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}" in result, "O conteúdo do texto foi perdido durante a refatoração."

    print("Teste de refatoração AST concluído com sucesso.")