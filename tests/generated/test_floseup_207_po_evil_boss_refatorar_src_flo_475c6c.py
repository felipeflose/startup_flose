from flose.solutions.floseup_207_po_evil_boss_refatorar_src_flo_475c6c import *

import asyncio
import pytest

@pytest.mark.asyncio
async def test_po_evil_boss_refarar_sr():
    """
    Testa a função refatorada po_evil_boss_refarar_sr para garantir que a lógica de auditoria seja executada corretamente.
    """
    # 1. Setup de dados de teste
    test_data = [
        {"id": 1, "status": "passed"},
        {"id": 2, "status": "failed"},
        {"id": 3, "status": "passed"},
    ]

    # 2. Execução da função refatorada
    result = await po_evil_boss_refarar_sr()

    # 3. Verificação dos resultados esperados
    expected_results = {
        1: "Compliance Passed",
        2: "Compliance Failed",
        3: "Compliance Passed",
    }

    assert result == expected_results
    assert isinstance(result, dict)
    assert len(result) == 3