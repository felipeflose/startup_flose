def po_evil_boss_refatorar_sr(code_snippet: str) -> str:
    """
    Visão de Negócio: Refatorar o estilo inline extenso em código de template para CSS modular (HSL classes), melhorando a manutenibilidade e a consistência do frontend.
    Visão Técnica AST: Substituir o estilo inline diretamente na string de código HTML pelo uso de classes CSS pré-definidas, extraindo as propriedades de estilo para um contexto HSL.
    """
    # Definir as classes CSS baseadas no estilo inline original
    # Estilo original: font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;
    # Mapeamento HSL:
    # font-size: 0.38rem -> (Assume a scale, e.g., scale(1.2) for base size)
    # color: #ff5555 (Orange/Red)
    # margin-bottom: 0.2rem
    
    css_classes = "po-rejection-reason-style"
    
    # O trecho a ser substituído: <div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">...</div>
    
    # Substituição do estilo inline pela classe CSS
    new_code_snippet = code_snippet.replace(
        '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">',
        f'<div class="{css_classes}">'
    )
    
    # Ajustar o conteúdo interno (mantendo o conteúdo)
    # Note: A substring(0, 50) é parte do conteúdo que deve ser preservado.
    # O conteúdo interno é: '💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}'
    
    # A string original é: `${duel.active_card.po_rejection_reason ? '<div style="...">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>' : ''}`
    
    # Refatorando a parte do HTML
    
    # O bloco de código que será refatorado é o conteúdo entre o ? e o :
    
    if code_snippet.startswith("${duel.active_card.po_rejection_reason"):
        # Se a condição for True, refatorar o HTML
        
        # Encontrar e substituir o estilo inline
        # Este regex/substituição precisa ser robusta para o contexto exato.
        
        # Vamos refatorar o trecho exato fornecido:
        
        # Original: `<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>`
        
        # Substituindo o estilo inline pela classe
        refactored_html = code_snippet.replace(
            '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">',
            f'<div class="{css_classes}">'
        )
        
        # Garantir que o fechamento da div também seja tratado se necessário, mas o foco é a remoção do style.
        
        # Reconstruindo a string final com a classe
        final_result = code_snippet.replace(
            '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">',
            f'<div class="{css_classes}">'
        )
        
        return final_result
    
    return code_snippet


import pytest

# Simulação da string de código que seria analisada (mockando o contexto)
MOCK_CODE_SNIPPET = `${duel.active_card.po_rejection_reason ? '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>' : ''}`

def test_po_evil_boss_refatorar_sr():
    """Verifica se a função refatora corretamente o estilo inline para classes CSS."""
    
    expected_css_class = "po-rejection-reason-style"
    
    refactored_code = po_evil_boss_refatorar_sr(MOCK_CODE_SNIPPET)
    
    # Esperamos que o estilo inline tenha sido substituído pela classe CSS.
    assert expected_css_class in refactored_code
    assert 'style="' not in refactored_code
    assert f'<div class="{expected_css_class}"' in refactored_code
    assert 'font-size:0.38rem' not in refactored_code
    assert 'color:#ff5555' not in refactored_code
    assert 'margin-bottom:0.2rem' not in refactored_code
    
    print(f"Refatorado: {refactored_code}")