from flose.solutions.floseup_199_po_evil_boss_refatorar_src_flo_44a452 import *

def test_refactoring_success():
    """
    Testa se a função po_evil_boss_refatorar_sr realiza a refatoração esperada.
    """
    # Configuração (simulada)
    expected_prefix = "👔 <b>Felipe:</b> Analisou & Delegou para "
    expected_suffix = "</span>!"
    expected_class = 'hero-color-primary'

    # Execução da função
    result = po_evil_boss_refatorar_sr()

    # Verificação dos critérios de aceite
    assert expected_prefix in result, "O prefixo da string não foi mantido."
    assert f'class="{expected_class}"' in result, "A classe CSS modular não foi aplicada corretamente."
    assert expected_suffix in result, "O sufixo da string não foi mantido."
    assert "${duel.active_hero}" in result, "A variável dinâmica não foi preservada."

if __name__ == '__main__':
    test_refactoring_success()