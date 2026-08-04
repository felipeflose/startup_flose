from flose.solutions.floseup_219_po_evil_boss_refatorar_src_flo_4070ae import *

def test_po_evil_boss_refatorar_sr():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que a refatoração
    de estilos inline para classes CSS HSL foi aplicada corretamente.
    """
    # Setup
    result = po_evil_boss_refatorar_sr()

    # Assumindo que o input simulado é o conteúdo que seria inserido
    test_content = "Conteúdo de teste"

    # Teste 1: Condição True (com conteúdo)
    expected_output_true = f'<div class="{po_evil_boss_refatorar_sr.__globals__["CSS_CLASSES"]["po_evil_boss_style"]}">{test_content}</div>'
    
    # Nota: Como a função acima retorna uma função, precisamos chamar a lógica interna para teste
    actual_output_true = po_evil_boss_refatorar_sr(test_content)
    
    assert actual_output_true == expected_output_true, "Teste falhou para o caso True"

    # Teste 2: Condição False (vazio)
    actual_output_false = po_evil_boss_refatorar_sr("")
    
    assert actual_output_false == '', "Teste falhou para o caso False"

    print("Todos os testes para po_evil_boss_refatorar_sr foram aprovados.")