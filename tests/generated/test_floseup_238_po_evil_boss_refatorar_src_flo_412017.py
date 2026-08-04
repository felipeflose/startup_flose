import pytest
from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_412017 import po_evil_boss_refatorar_sr

def test_refactoring_function():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que ela refatora corretamente
    o estilo inline para uma classe modular.
    """
    # Simulação do código original que será processado
    original_code = '<span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>'
    
    # Esperamos que a função retorne o código refatorado
    expected_output = '<span class="xp-style">XP: ${a.xp || 0}%</span>'
    
    result = po_evil_boss_refatorar_sr(original_code)
    
    assert result == expected_output