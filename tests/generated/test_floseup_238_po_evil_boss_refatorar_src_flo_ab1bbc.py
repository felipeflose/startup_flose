from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_ab1bbc import *

def test_po_evil_boss_refatorar_sr():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que a refatoração
    do estilo inline para classes HSL foi realizada corretamente.
    """
    result = po_evil_boss_refatorar_sr()

    # Verificação da refatoração do estilo
    assert result['original_style'] == "color:#a855f7; float:right;"
    assert result['new_css_class'] == "xp-style-evil-boss"
    
    # Verificação da geração do CSS modular
    expected_css = ".xp-style-evil-boss { color: #a855f7; float: right; }"
    assert result['css_definition'] == expected_css
    
    # Verificação do resultado HTML refatorado
    expected_html = '<span class="xp-style-evil-boss">XP: ${a.xp || 0}%</span>'
    assert result['refactored_html'] == expected_html

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr()