from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_6a82b5 import *

def test_po_evil_boss_refatorar_sr():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que o estilo inline seja substituído por classes CSS.
    """
    # Teste com dados de entrada simulados
    input_text = "XP: ${a.xp || 0}%"
    
    # Esperado: A função deve injetar a classe CSS modular no span
    expected_class = "text-purple-500 float-right"
    
    result = po_evil_boss_refatorar_sr()
    
    # Verificação se o resultado contém a classe CSS esperada
    assert expected_class in result
    assert input_text in result
    
    # Verificação mais específica da estrutura esperada
    assert result.startswith('<span class="')
    assert result.endswith('">')

if __name__ == '__main__':
    # Este bloco é opcional, mas útil para rodar o teste diretamente
    test_po_evil_boss_refatorar_sr()