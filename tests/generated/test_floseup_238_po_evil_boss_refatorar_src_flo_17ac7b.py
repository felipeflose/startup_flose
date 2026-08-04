import pytest
from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_17ac7b import po_evil_boss_refatorar_sr

def test_refactor_functionality():
    """
    Testa se a função po_evil_boss_refatorar_sr refatora corretamente o estilo inline
    para classes CSS com valores HSL.
    """
    # Input simulado baseado no código real do Jira (Linha 1616)
    input_code = '<span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>'

    # Esperamos que o resultado contenha a classe HSL e a propriedade float
    expected_prefix = '<span class="style="color:hsl(171, 255, 247); float:right;">'

    result = po_evil_boss_refatorar_sr(input_code)

    # Verificações
    assert result.startswith(expected_prefix)
    assert "XP: ${a.xp || 0}%" in result
    assert "color:hsl(171, 255, 247)" in result
    assert "float:right" in result