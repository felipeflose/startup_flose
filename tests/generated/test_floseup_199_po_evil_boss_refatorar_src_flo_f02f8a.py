from flose.solutions.floseup_199_po_evil_boss_refatorar_src_flo_f02f8a import *

import pytest

def test_po_evil_boss_refatorar_sr():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que ela refatore o estilo inline
    para uma classe CSS modular.
    """
    # 1. Executar a função
    refactored_code, css_class_name = po_evil_boss_refatorar_sr()

    # 2. Verificação da refatoração
    # Esperamos que o estilo inline tenha sido removido e substituído por uma classe.
    assert "style=\"color:#a855f7;\"" not in refactored_code
    assert f'class="{css_class_name}"' in refactored_code
    
    # Verificação da lógica de extração (simulada)
    assert css_class_name == "text-purple-500"

# Nota: Em um ambiente real, se a função po_evil_boss_refatorar_sr fosse async,
# o teste seria definido como async def test_po_evil_boss_refatorar_sr().