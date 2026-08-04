from flose.solutions.floseup_219_po_evil_boss_refatorar_src_flo_18474f import *

def test_po_evil_boss_refatorar_sr():
    # Simulação de dados de teste para verificar a lógica de refatoração
    
    # Caso 1: O campo existe e tem valor
    test_data_1 = {
        "duel": type('Duel', (object,), {'active_card': type('Card', (object,), {'po_rejection_reason': "Este é um motivo de rejeição longo que deve ser cortado para caber no limite"})})()
    }
    
    # Testando com dados que resultariam na string esperada se a função fosse chamada com o contexto correto
    result_1 = po_evil_boss_refatorar_sr(po_rejection_reason=test_data_1.duel.active_card.po_rejection_reason)
    
    expected_1 = '<div class="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 Este é um motivo de rejeição longo que deve ser cortado para caber no limite</div>'

    # Nota: Devido à natureza da função de refatoração simulada acima, que aplica classes diretamente,
    # o teste verifica se a lógica de extração e aplicação das classes foi correta.
    assert result_1 == expected_1, "Teste 1 falhou: A refatoração do estilo inline não gerou a string CSS esperada."

    # Caso 2: O campo não existe ou é nulo
    test_data_2 = {
        "duel": type('Duel', (object,), {'active_card': type('Card', (object,), {'po_rejection_reason': None})})()
    }
    result_2 = po_evil_boss_refatorar_sr(po_rejection_reason=test_data_2.duel.active_card.po_rejection_reason)
    
    expected_2 = ''
    assert result_2 == expected_2, "Teste 2 falhou: O tratamento de valor nulo não resultou em string vazia."

    print("Todos os testes para po_evil_boss_refatorar_sr foram aprovados.")