from flose.solutions.floseup_142_po_evil_boss_refatorar_src_flo_85ea39 import *

def test_po_evil_boss_refatorar_sr():
    # Simulação do trecho de código que seria processado
    original_code = (
        "${c.rejections > 0 && !c.po_rejection_reason ? "
        "<div style=\"color:#ff5555; font-size:0.3rem;\">⚠️ ${c.rejections}x rejeitado</div>" 
        ": ''}"
    )
    
    # Testando a função de refatoração
    refactored_code = po_evil_boss_refatorar_sr(original_code)
    
    # Verificação da refatoração
    expected_refactoring = (
        "${c.rejections > 0 && !c.po_rejection_reason ? "
        "<div class=\"rejection-warning\">⚠️ ${c.rejections}x rejeitado</div>" 
        ": ''}"
    )
    
    assert refactored_code == expected_refactoring, "A string de template não foi refatorada corretamente para usar classes CSS."