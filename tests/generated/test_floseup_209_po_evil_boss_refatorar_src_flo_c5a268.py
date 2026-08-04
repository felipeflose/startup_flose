from flose.solutions.floseup_209_po_evil_boss_refatorar_src_flo_c5a268 import *

def test_po_evil_boss_refatorar_sr():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que a refatoração de estilos inline para classes CSS foi realizada corretamente.
    """
    # Simulação da execução da função
    result = po_evil_boss_refatorar_sr()

    # Verificação de que a string resultante segue o padrão de classes CSS
    expected_start = '<div class='
    assert result.startswith(expected_start)
    assert 'base_text_style' in result
    assert 'phase_color_style' in result
    assert 'margin_bottom_style' in result

    # Verificação de que os estilos inline foram removidos
    assert 'style=' not in result

    print("Refatoração de estilo realizada com sucesso.")