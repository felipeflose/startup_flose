from flose.solutions.floseup_209_po_evil_boss_refatorar_src_flo_57ceff import *

def test_po_evil_boss_refatorar_sr_refactoring():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que ela refatore corretamente o estilo inline em classes.
    """
    result = po_evil_boss_refatorar_sr()

    # Verificação da extração das classes geradas
    expected_classes = "size-052rem color-dynamic weight-bold margin-bottom-025rem text-center"
    
    assert result['original_style'] == "font-size:0.52rem; color:${phaseColor}; font-weight:bold; margin-bottom:0.25rem; text-align:center;"
    assert result['refactored_classes'] == expected_classes
    
    # Verificação da estrutura do resultado
    assert 'refactored_html_snippet' in result
    assert result['refactored_html_snippet'].startswith('<div class=')
    
    print("Refatoração realizada com sucesso e classes geradas corretamente.")