from flose.solutions.floseup_234_po_evil_boss_refatorar_src_flo_b1c8a5 import po_evil_boss_refatorar_sr

import asyncio

async def test_po_evil_boss_refatorar_sr():
    """Testa a refatoração da função de síntese de código."""
    agent_name = "Gemma4"
    topic = "Refactoring"
    description = "Modularize a função principal."
    slug = "refactor_task"

    # Teste da função refatorada
    result_code, result_text = await po_evil_boss_refatorar_sr()

    # Verificação básica para garantir que a função foi chamada e retornou algo
    assert isinstance(result_code, str)
    assert isinstance(result_text, str)
    assert "Synthesized code" in result_code
    assert "Processed response" in result_text

if __name__ == "__main__":
    asyncio.run(test_po_evil_boss_refatorar_sr())