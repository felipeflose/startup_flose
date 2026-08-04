from flose.solutions.floseup_238_po_evil_boss_refatorar_src_flo_937b14 import *

def test_refactoring_success():
    """Testa se a função po_evil_boss_refatorar_sr implementa a refatoração esperada."""
    # Nota: Como a função acima é uma simulação baseada no enunciado,
    # o teste verifica se a lógica de refatoração foi executada corretamente
    # no contexto da string de exemplo.
    
    # Simulação da execução da função com o código de exemplo
    result = po_evil_boss_refatorar_sr()
    
    # Verificação da saída esperada (baseada na refatoração simulada)
    expected_output_fragment = '<span class="xp-value-a855f7 float:right">XP: ${a.xp || 0}%</span>'
    
    assert expected_output_fragment in result, "O resultado da refatoração não contém a classe CSS esperada."
    print("Teste de refatoração AST executado com sucesso.")

if __name__ == '__main__':
    test_refactoring_success()