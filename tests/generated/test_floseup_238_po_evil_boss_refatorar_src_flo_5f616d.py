from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_5f616d import *

def test_po_evil_boss_refatorar_sr_refactoring():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que ela extrai corretamente o estilo inline
    e gera a definição CSS modular necessária.
    """
    result = po_evil_boss_refatorar_sr()

    # Verificação da extração do estilo
    assert result["original_style"] == "color:#a855f7; float:right;", "O estilo inline não foi extraído corretamente."

    # Verificação da definição da classe CSS
    expected_css = """
.xp-label-styled {
    color: #a855f7;
    float: right;
}
"""
    assert result["css_definition"].strip() == expected_css.strip(), "A definição CSS modular está incorreta."

    # Verificação do snippet refatorado
    expected_snippet = '<span class="xp-label-styled">XP: ${a.xp || 0}%</span>'
    assert result["refactored_snippet"] == expected_snippet, "O snippet refatorado não corresponde à expectativa."

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr_refactoring()