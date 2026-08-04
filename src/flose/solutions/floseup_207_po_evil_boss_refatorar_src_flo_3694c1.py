"""
Visão de Negócio: Modularizar a corotina de auditoria de conformidade para melhorar a manutenibilidade, testabilidade e o gerenciamento de estado assíncrono.
Visão Técnica AST: Refatorar a função 'background_compliance_auditor_worker' em um conjunto de funções menores e focadas, permitindo que cada etapa da auditoria seja testada de forma isolada.
"""
import asyncio
from typing import List, Dict, Any

async def _perform_compliance_check(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Simula a checagem de conformidade para um lote de dados."""
    await asyncio.sleep(0.1)  # Simula I/O bound operation
    results = []
    for item in data:
        if item.get('status') == 'compliant':
            results.append({'id': item['id'], 'status': 'PASSED', 'details': 'Compliance OK'})
        else:
            results.append({'id': item['id'], 'status': 'FAILED', 'details': 'Compliance Issue'})
    return results

async def _process_audit_batch(batch_id: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Processa um lote de dados, realizando a checagem de conformidade."""
    print(f"Iniciando processamento do lote: {batch_id}")
    compliance_results = await _perform_compliance_check(data)
    total_failed = sum(1 for res in compliance_results if res['status'] == 'FAILED')
    return {
        "batch_id": batch_id,
        "total_items": len(data),
        "failed_items": total_failed,
        "results": compliance_results
    }

async def background_compliance_auditor_worker(batches: List[Dict[str, Any]]):
    """
    Função principal refatorada para orquestrar a auditoria de conformidade de forma modular.
    """
    print("Iniciando o worker de auditoria de conformidade.")
    tasks = []
    for batch in batches:
        # Cria tarefas separadas para cada lote
        task = _process_audit_batch(batch['id'], batch['data'])
        tasks.append(task)

    # Executa todas as tarefas em paralelo
    results = await asyncio.gather(*tasks)

    final_report = {
        "status": "COMPLETED",
        "batch_reports": results
    }
    print("Auditoria de conformidade concluída.")
    return final_report

# --- Bloco Pytest ---

import pytest
import asyncio
from flose.solutions.floseup_207_po_evil_boss_refatorar_src_flo_3694c1 import *

@pytest.mark.asyncio
async def test_po_evil_boss_refar_sr():
    """Testa se a função principal executa as tarefas de forma assíncrona e retorna o resultado esperado."""
    
    # 1. Setup de dados de teste
    mock_batches = [
        {'id': 'B001', 'data': [
            {'id': 1, 'status': 'compliant'},
            {'id': 2, 'status': 'failed'}
        ]},
        {'id': 'B002', 'data': [
            {'id': 3, 'status': 'compliant'},
            {'id': 4, 'status': 'compliant'}
        ]}
    ]

    # 2. Execução da função refatorada
    report = await po_evil_boss_refar_sr(mock_batches)

    # 3. Verificação dos critérios de aceite
    assert report['status'] == "COMPLETED"
    assert len(report['batch_reports']) == 2

    # Verificação do primeiro lote (B001)
    report_b001 = next(item for item in report['batch_reports'] if item['batch_id'] == 'B001')
    assert report_b001['total_items'] == 2
    assert report_b001['failed_items'] == 1
    assert len(report_b001['results']) == 2
    assert any(res['status'] == 'FAILED' for res in report_b001['results'])
    
    # Verificação do segundo lote (B002)
    report_b002 = next(item for item in report['batch_reports'] if item['batch_id'] == 'B002')
    assert report_b002['total_items'] == 2
    assert report_b002['failed_items'] == 0
    assert all(res['status'] == 'PASSED' for res in report_b002['results'])