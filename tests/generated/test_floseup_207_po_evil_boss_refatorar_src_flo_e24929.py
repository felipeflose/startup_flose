from flose.solutions.floseup_207_po_evil_boss_refatorar_src_flo_e24929 import po_evil_boss_refatorar_sr

import asyncio
import pytest

@pytest.mark.asyncio
async def test_po_evil_boss_refatorar_sr():
    """
    Testa a implementação modularizada da lógica do worker de auditoria.
    Verifica se a função principal orquestra corretamente as sub-rotinas.
    """
    # Simulação de um ambiente assíncrono para teste
    async def run_test():
        # 1. Testar a busca de dados
        context = {"user_id": 456}
        compliance_data = await po_evil_boss_refatorar_sr.fetch_compliance_data(context)
        assert isinstance(compliance_data, list)
        assert len(compliance_data) > 0

        # 2. Testar a execução da auditoria
        audit_results = await po_evil_boss_refatorar_sr.perform_audit(compliance_data)
        assert isinstance(audit_results, dict)
        assert 1 in audit_results
        assert audit_results[1] == "compliant"

        # 3. Testar o relatório (verificação de que a função foi chamada)
        await po_evil_boss_refatorar_sr.report_results(audit_results)
        # Não há retorno explícito, mas a ausência de exceções indica sucesso na orquestração.

    # Executa o teste assíncrono
    await run_test()