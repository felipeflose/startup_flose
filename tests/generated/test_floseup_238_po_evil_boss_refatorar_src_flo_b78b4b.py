from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_b78b4b import *

def test_po_evil_boss_refatorar_sr():
    # Setup: Simular o código real do arquivo para teste
    original_code = '<span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>'
    
    # Execução
    refactored_code = po_evil_boss_refatorar_sr(original_code)
    
    # Assertions
    # Esperamos que o estilo inline tenha sido substituído por uma classe modular.
    expected_class_prefix = "text-a855f7-highlight"
    assert expected_class_prefix in refactored_code
    
    # Verificação da estrutura refatorada
    assert refactored_code.startswith('<span class="')
    assert refactored_code.endswith('</span>')
    
    # Verificação do conteúdo
    assert "XP: ${a.xp || 0}%" in refactored_code

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr()