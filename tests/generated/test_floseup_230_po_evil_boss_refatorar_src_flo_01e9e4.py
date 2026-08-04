from flose.solutions.floseup_230_po_evil_boss_refatorar_src_flo_01e9e4 import po_evil_boss_refatorar_sr

import pytest
from unittest.mock import patch

def test_po_evil_boss_refatorar_sr_exception_handling():
    # Teste de refatoração para a exceção genérica
    result = po_evil_boss_refatorar_sr(
        "result = 1 / 0",
        Exception,
        "Erro de execução geral"
    )
    
    # Verificamos se a string refatorada contém a lógica de logging, demonstrando a mudança
    assert "except Exception as e:" in result
    assert "logger.error(f'Erro inesperado durante a operação: Erro de execução geral. Detalhes: {e}')" in result

def test_po_evil_boss_refatorar_sr_specific_exception_handling():
    # Teste de refatoração para uma exceção específica
    result = po_evil_boss_refatorar_sr(
        "result = 1 / 0",
        ZeroDivisionError,
        "Erro de divisão por zero"
    )
    
    # Verificamos se a string refatorada contém o tratamento específico
    assert "except ZeroDivisionError:" in result
    assert "logger.warning(f'Erro específico capturado: Erro de divisão por zero')" in result