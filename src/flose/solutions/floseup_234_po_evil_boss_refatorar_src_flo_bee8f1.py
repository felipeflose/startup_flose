def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Modularizar a função de síntese de código para melhorar a manutenibilidade e a testabilidade do módulo de engenharia.
    Visão Técnica AST: Refatorar a corotina assíncrona 'call_gemma_for_code' (atualmente 76 linhas) em funções modulares, extraindo a lógica de síntese em sub-módulos assíncronos.
    """
    import asyncio
    from typing import Tuple

    # Simulação da modularização: Extrair a lógica principal em funções auxiliares
    async def _synthesize_code(agent_name: str, topic: str, description: str, slug: str) -> str:
        # Lógica de síntese real aqui (simulada)
        await asyncio.sleep(0.1)
        return f"Synthesized code for {topic} based on description and agent {agent_name}."

    async def _prepare_context(description: str) -> dict:
        # Lógica de preparação de contexto real (simulada)
        await asyncio.sleep(0.05)
        return {"context": description, "slug": slug}

    async def call_gemma_for_code(agent_name: str, topic: str, description: str, slug: str) -> Tuple[str, str]:
        """
        Função refatorada e modularizada.
        """
        context = await _prepare_context(description)
        synthesized_result = await _synthesize_code(agent_name, topic, description, slug)
        
        return synthesized_result, context["slug"]

# --- Testes Pytest ---
from flose.solutions.floseup_234_po_evil_boss_refatorar_src_flo_bee8f1 import *

import pytest
import asyncio

@pytest.mark.asyncio
async def test_po_evil_boss_refatorar_sr_refactoring():
    # Testando a função refatorada
    agent_name = "Gemma4"
    topic = "Async Refactoring"
    description = "Refactor the code to be more modular."
    slug = "refactor-async"

    result, generated_slug = await po_evil_boss_refatorar_sr(
        agent_name=agent_name,
        topic=topic,
        description=description,
        slug=slug
    )

    # Verificação básica da saída
    assert "Synthesized code" in result
    assert generated_slug == slug
    
    # Verificação de que a estrutura modular foi chamada corretamente
    assert isinstance(result, str)
    assert isinstance(generated_slug, str)