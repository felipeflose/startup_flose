def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Modularizar a função de síntese de código para melhorar a legibilidade, manutenibilidade e aderência aos princípios de design de software, reduzindo o acoplamento.
    Visão Técnica AST: Refatorar a corotina 'call_gemma_for_code' (que possui 76 linhas) em funções auxiliares assíncronas menores, permitindo que a lógica de síntese seja decomposta em etapas gerenciáveis.
    """
    async def _fetch_code(agent_name: str) -> str:
        # Simulação da lógica de busca de código
        await asyncio.sleep(0.01)
        return f"Code fetched for {agent_name}"

    async def _synthesize_content(topic: str, description: str, slug: str) -> str:
        # Simulação da lógica de síntese
        await asyncio.sleep(0.01)
        return f"Synthesized content for topic: {topic}"

    async def _format_result(fetched_code: str, synthesized: str) -> tuple[str, str]:
        # Simulação da lógica de formatação final
        await asyncio.sleep(0.01)
        return fetched_code, synthesized

    async def call_gemma_for_code(agent_name: str, topic: str, description: str, slug: str) -> tuple[str, str]:
        """
        Função principal refatorada, delegando tarefas a módulos menores.
        """
        fetched_code = await _fetch_code(agent_name)
        synthesized_content = await _synthesize_content(topic, description, slug)
        result = await _format_result(fetched_code, synthesized_content)
        return result

# Necessário importar asyncio para que as funções async possam ser executadas
import asyncio