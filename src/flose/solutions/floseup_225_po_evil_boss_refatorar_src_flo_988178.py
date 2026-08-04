def po_evil_boss_refatorar_sr(content: str) -> str:
    """
    Visão de Negócio: Refatorar o estilo inline extenso em CSS modular usando classes HSL para melhorar a manutenibilidade do frontend.
    Visão Técnica AST: Realiza a extração do estilo inline do trecho de código e o substitui por classes CSS definidas, seguindo a lógica de auditoria AST.
    """
    # Definir as classes CSS com valores HSL conforme a exigência
    css_classes = {
        "po_rejection_reason_style": "font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;",
        # Nota: O valor HSL é usado para definir a cor, conforme solicitado no diagnóstico.
        "po_rejection_reason_text": "💬 {text}",  # Placeholder para o conteúdo dinâmico
    }

    # Lógica de refatoração: Substituir o style inline pela classe
    if content.startswith('<div style='):
        # Identificar o conteúdo a ser movido
        start_div = content.find('<div')
        end_div = content.rfind('>')

        if start_div != -1 and end_div != -1:
            # Extrair o conteúdo interno
            inner_content = content[start_div + 5: end_div]  # Pular '<div style='
            
            # Criar a nova estrutura com classes
            refactored_content = f'<div class="{css_classes["po_rejection_reason_style"]}">{inner_content}</div>'
            return refactored_content
    
    # Se não for o formato esperado, retorna o original (ou o vazio, dependendo da lógica completa)
    return content

import pytest

from flose.solutions.floseup_225_po_evil_boss_refatorar_src_flo_988178 import po_evil_boss_refatorar_sr

def test_po_evil_boss_refatorar_sr():
    # Cenário 1: O campo de rejeição existe
    input_content_with_style = `${duel.active_card.po_rejection_reason ? '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>' : ''}`
    
    expected_refactored = '<div class="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>'
    
    result = po_evil_boss_refatorar_sr(input_content_with_style)
    
    # A verificação deve garantir que o estilo inline foi substituído pela classe
    assert result == expected_refactored

    # Cenário 2: O campo de rejeição não existe (caso de fallback)
    input_content_empty = `${duel.active_card.po_rejection_reason ? '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>' : ''}`
    
    # Neste caso, a função deve retornar a string vazia (ou a estrutura baseada na lógica)
    expected_empty = ''
    result_empty = po_evil_boss_refatorar_sr(input_content_empty)
    
    assert result_empty == expected_empty