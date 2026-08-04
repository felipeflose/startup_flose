from flose.solutions.floseup_209_po_evil_boss_refatorar_src_flo_032e6e import po_evil_boss_refatorar_sr

import pytest

def test_refactoring_function():
    # Testando a função de refatoração
    result = po_evil_boss_refatorar_sr()

    # Verificação básica para garantir que a função retornou uma string formatada
    assert isinstance(result, str)
    assert "class" in result
    assert "font-size: 0.52rem" in result
    assert "margin-bottom: 0.25rem" in result
    assert "color: " in result  # Verifica se a variável dinâmica foi incorporada