from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_68b890 import *

def test_po_evil_boss_refatorar_sr():
    """
    Testa a função de refatoração para garantir que o estilo inline foi substituído por classes CSS.
    """
    # Executa a função de refatoração
    result = po_evil_boss_refatorar_sr()
    
    # Verificação: Deve conter classes CSS e não o estilo inline.
    assert "class=" in result
    assert "float:right;" in result
    assert "color:hsl(270, 70%, 60%);" in result
    assert "style=" not in result
    assert "XP: ${a.xp || 0}%" in result