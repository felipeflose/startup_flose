from flose.solutions.floseup_209_po_evil_boss_refatorar_src_flo_f31414 import *
import pytest

def test_refactored_code():
    with open('src/flose/web_app.py', 'r') as file:
        code = file.read()

    # Verifica se as classes CSS foram adicionadas corretamente
    assert '<style>.custom_phaseColor{font-size:0.52rem; color:hsl(180, 100%, 50%); font-weight:bold; margin-bottom:0.25rem; text-align:center;}</style>' in code

    # Verifica se o estilo inline foi removido
    assert 'style="font-size:0.52rem; color:hsl(180, 100%, 50%); font-weight:bold; margin-bottom:0.25rem; text-align:center;"' not in code

    # Verifica se o Jinja2Template foi corretamente refatorado
    assert 'class="{{ " ".join(css_classes) }}"' in code

test_refactored_code()