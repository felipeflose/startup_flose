from flose.solutions.floseup_199_po_evil_boss_refatorar_src_flo_c4bce2 import *

def test_po_evil_boss_refatorar_sr():
    """
    Testa a função de refatoração para garantir que o estilo inline foi substituído por uma classe CSS modular.
    """
    # Simulação da linha problemática conforme a descrição
    original_line = "👔 <b>Felipe:</b> Analisou & Delegou para <span style=\"color:#a855f7;\">${duel.active_hero}</span>!"
    
    # Executar a função de refatoração
    refactored_line = po_evil_boss_refatorar_sr(original_line)
    
    # Verificação esperada: O estilo inline deve ter sido substituído pela classe CSS
    expected_refactor = "👔 <b>Felipe:</b> Analisou & Delegou para <span class=\"text-purple-500;\">${duel.active_hero}</span>!"
    
    assert refactored_line == expected_refactor, "A refatoração não gerou a string esperada."
    print("Teste de refatoração AST bem-sucedido.")