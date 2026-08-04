from flose.solutions.floseup_219_po_evil_boss_refatorar_src_flo_860c4e import *

def test_po_evil_boss_refatorar_sr():
    # Teste de caso onde o conteúdo existe
    input_content = "${duel.active_card.po_rejection_reason ? `<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>` : ''}"
    
    expected_output = '<div class="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>'
    
    result = po_evil_boss_refatorar_sr(input_content)
    
    # A refatoração deve substituir o estilo inline pela classe modular
    # Nota: Como o input é uma string complexa, testamos a lógica de extração e aplicação da classe.
    assert "class=" in result, "O resultado deve conter uma classe."
    assert "font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;" in result, "As classes HSL devem ser aplicadas corretamente."
    assert "💬" in result, "O conteúdo dinâmico deve ser mantido."
    
    # Verificação específica da refatoração (simulando o resultado esperado da função)
    # Se a função fosse refatorar o *conteúdo* da string, o resultado seria:
    expected_refactored = '<div class="rejection_reason_style">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>'
    
    # Como a função implementada acima refatora o estilo inline para uma classe, testamos o resultado esperado da lógica interna.
    # Ajustando o teste para refletir a lógica implementada no primeiro bloco:
    assert po_evil_boss_refatorar_sr(input_content) == expected_refactored
    
    # Teste de caso onde o conteúdo é vazio
    empty_input = ""
    assert po_evil_boss_refatorar_sr(empty_input) == ""