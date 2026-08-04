from flose.solutions.floseup_158_po_evil_boss_refatorar_src_flo_a1dcd7 import *

def test_po_evil_boss_refatorar_sr():
    """
    Verifica se a função de refatoração implementa a substituição de estilos inline por classes CSS.
    """
    # Simulação de dados de entrada para teste
    mock_duel = type('obj', (object,), {
        'active_card': type('card', (object,), {
            'po_rejection_reason': type('reason', (object,), {
                'substring': lambda x: "REJECTION_REASON_TEXT"
            })
        })
    })()

    # Execução da função
    result = po_evil_boss_refatorar_sr()

    # Verificação da refatoração
    expected_class_style = "font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;"

    # O teste verifica se a estrutura foi alterada para usar classes em vez de style inline
    assert "class" in result, "O resultado deve conter classes CSS em vez de estilo inline."
    assert expected_class_style in result, "As propriedades de estilo HSL devem estar presentes na classe aplicada."
    assert "style=" not in result, "O atributo style inline deve ter sido removido."

if __name__ == '__main__':
    test_po_evil_boss_refatorar_sr()