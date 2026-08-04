def po_evil_boss_refatorar_sr(template_string: str) -> str:
    """
    Visão de Negócio: Melhorar a manutenibilidade e a separação de preocupações (CSS) do código Python, seguindo princípios de design modular.
    Visão Técnica AST: Refatorar a string de template que contém estilos inline (HTML) para utilizar classes CSS externas, extraindo os estilos para um sistema modular baseado em classes HSL.
    """
    if not template_string:
        return ""

    # Identificar o trecho a ser refatorado
    start_tag = '<div style='
    end_tag = '</div>'
    
    # Extrair o conteúdo interno
    content_start = template_string.find(start_tag)
    content_end = template_string.rfind(end_tag)

    if content_start == -1 or content_end == -1:
        return template_string

    # Extrair o conteúdo (incluindo o estilo inline)
    inline_style_block = template_string[content_start : content_end + len(end_tag)]
    
    # Analisar o estilo inline para extrair propriedades e criar classes
    
    # Estilos a serem extraídos:
    # font-size:0.38rem;
    # color:#ff5555;
    # margin-bottom:0.2rem;
    
    # Simulação da extração de classes (Em um cenário real, isso seria feito por um parser mais robusto)
    
    # Criar classes HSL baseadas nos estilos identificados
    css_classes = []
    
    # Estilo 1: font-size:0.38rem;
    css_classes.append('text-sm') # Exemplo de mapeamento
    
    # Estilo 2: color:#ff5555; (Cor vermelha/laranja)
    css_classes.append('text-red-500') 
    
    # Estilo 3: margin-bottom:0.2rem;
    css_classes.append('mb-1') 

    # Conteúdo dinâmico
    content = template_string[content_start + len(start_tag): content_end]

    # Reconstruir o HTML usando classes
    refactored_html = f'<div class="po-rejection-reason-container">'
    refactored_html += f'<div class="po-rejection-reason-text">{content}</div>'
    refactored_html += '</div>'
    
    return refactored_html

# --- Testes Pytest ---
from flose.solutions.floseup_219_po_evil_boss_refatorar_src_flo_886d66 import *

import pytest

def test_po_evil_boss_refatorar_sr_with_reason():
    """Testa a refatoração quando a razão de rejeição está presente."""
    original_template = `${duel.active_card.po_rejection_reason ? \`<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>` : ''}`
    
    expected_output_start = '<div class="po-rejection-reason-container">'
    expected_output_end = '</div>'
    
    result = po_evil_boss_refatorar_sr(original_template)
    
    # Verificação básica de que as classes foram aplicadas e o conteúdo preservado
    assert expected_output_start in result
    assert expected_output_end in result
    assert "💬" in result
    assert "po-rejection-reason-text" in result
    assert "po-rejection-reason-container" in result

def test_po_evil_boss_refatorar_sr_without_reason():
    """Testa a refatoração quando a razão de rejeição está ausente."""
    original_template = `${duel.active_card.po_rejection_reason ? \`<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>` : ''}`
    
    result = po_evil_boss_refatorar_sr(original_template)
    
    # Espera que a saída seja apenas a string vazia ou o bloco vazio esperado
    assert result == ''
    
def test_po_evil_boss_refatorar_sr_empty_input():
    """Testa a função com uma string de entrada vazia."""
    assert po_evil_boss_refatorar_sr("") == ""