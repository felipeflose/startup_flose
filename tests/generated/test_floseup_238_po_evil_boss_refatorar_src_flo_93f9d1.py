import pytest
from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_93f9d1 import po_evil_boss_refatorar_sr

def test_refactoring_functionality():
    """
    Testa se a função po_evil_boss_refatorar_sr refatora corretamente o estilo inline para classes HSL.
    """
    # Input simulando o código da Linha 1616
    input_code = '<span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>'
    
    # Esperamos que a função extraia o estilo e o envolva em uma classe HSL
    expected_output = '<span class="style-hsl-a855f7">XP: ${a.xp || 0}%</span>'
    
    result = po_evil_boss_refatorar_sr(input_code)
    
    assert result == expected_output, "A função de refatoração não produziu o resultado esperado."

def test_refactoring_no_style():
    """
    Testa o caso onde não há estilo inline para garantir que a função lida corretamente.
    """
    input_code = 'XP: ${a.xp || 0}%'
    expected_output = 'XP: ${a.xp || 0}%' # Sem classes de estilo se não houver estilo
    
    result = po_evil_boss_refatorar_sr(input_code)
    
    assert result == expected_output, "A função falhou ao lidar com código sem estilo inline."