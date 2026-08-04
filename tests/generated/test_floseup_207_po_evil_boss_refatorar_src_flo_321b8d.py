from flose.solutions.floseup_207_po_evil_boss_refatorar_src_flo_321b8d import po_evil_boss_refatorar_sr

import asyncio
import pytest
from typing import List, Dict, Any

# Mock de dados para o teste
TEST_DATA = [
    {"id": 1, "status": "compliant", "data": "A"},
    {"id": 2, "status": "non_compliant", "data": "B"},
    {"id": 3, "status": "compliant", "data": "C"},
]

@pytest.mark.asyncio
async def test_po_evil_boss_refatorar_sr():
    """
    Testa a função refatorada po_evil_boss_refatorar_sr para garantir que ela processa os dados corretamente.
    """
    # Executa a função refatorada
    results = await po_evil_boss_refatorar_sr(TEST_DATA)
    
    # Verificação básica da lógica de processamento
    assert len(results) == len(TEST_DATA)
    
    # Verificação da lógica de compliance (baseado na simulação interna)
    compliant_count = sum(1 for item in results if item.get("is_compliant") is True)
    non_compliant_count = sum(1 for item in results if item.get("is_compliant") is False)
    
    assert compliant_count == 2
    assert non_compliant_count == 1
    
    # Verificação de que os dados originais foram processados
    for item in results:
        assert "id" in item
        assert "is_compliant" in item