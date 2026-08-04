from flose.solutions.floseup_142_po_evil_boss_refatorar_src_flo_51b805 import *

def test_po_evil_boss_refatorar_sr():
    # Setup simulado para testar a função refatoração
    template = (
        "${c.rejections > 0 && !c.po_rejection_reason ? "
        '<div style=\"color:#ff5555; font-size:0.3rem;\">⚠️ ${c.rejections}x rejeitado</div>" : ''}"
    )
    
    # Executar a refatoração
    result = po_evil_boss_refatorar_sr(template)
    
    # Verificação esperada
    expected = (
        "${c.rejections > 0 && !c.po_rejection_reason ? "
        '<div class=\"rejection_alert\">⚠️ ${c.rejections}x rejeitado</div>" : ''}"
    )
    
    # O teste deve verificar se a string foi alterada conforme a regra de refatoração
    assert result == expected, "A string de template não foi refatorada corretamente para usar classes CSS."