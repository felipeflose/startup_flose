from flose.solutions.floseup_199_po_evil_boss_refatorar_src_flo_2748ab import *

async def test_po_evil_boss_refatorar_sr():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que a refatoração do estilo inline para classes CSS HSL foi aplicada corretamente.
    """
    # Executa a função de refatoração
    result = po_evil_boss_refatorar_sr()
    
    # Verifica se a string refatorada contém a classe CSS esperada
    expected_class = 'text-purple-500'
    assert expected_class in result, f"A classe CSS esperada '{expected_class}' não foi encontrada no resultado da refatoração."
    
    # Verifica se o conteúdo principal foi mantido
    assert "Felipe: Analisou & Delegou para" in result
    assert "${duel.active_hero}" in result
    assert "<span>" in result
    
    print(f"Refatoração realizada com sucesso. Resultado: {result}")