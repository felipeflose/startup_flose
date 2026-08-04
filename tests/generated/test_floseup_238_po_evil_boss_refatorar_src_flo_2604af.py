from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_2604af import *

def test_po_evil_boss_refatorar_sr_refactoring():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que ela realiza a transformação esperada do estilo inline para classes CSS HSL.
    """
    # Setup: Simular o ambiente de teste
    
    # 1. Executar a função
    refactored_code, css_class = po_evil_boss_refatorar_sr()
    
    # 2. Assertions: Verificar se a lógica de refatoração foi aplicada corretamente
    
    # Verificar se a classe CSS foi gerada corretamente
    expected_color = "#a855f7"
    expected_css_class = f"xp-value-{expected_color}"
    
    assert css_class == expected_css_class, f"A classe CSS gerada está incorreta. Esperado: {expected_css_class}, Obtido: {css_class}"
    
    # Verificar se o código refatorado contém a aplicação da classe
    expected_refactoring = f"XP: ${a.xp || 0}% class=\"{expected_css_class}\""
    
    # Como a função simula a substituição, testamos a saída simulada
    assert refactored_code == expected_refactoring, f"O código refatorado não corresponde ao esperado. Esperado: {expected_refactoring}, Obtido: {refactored_code}"

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr_refactoring()