def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Melhorar a modularidade e a testabilidade da lógica de síntese de código, reduzindo a complexidade de uma única função assíncrona.
    Visão Técnica AST: Refatorar a função 'call_gemma_for_code' em módulos menores, extraindo a lógica de geração de código e processamento de entrada para funções separadas, facilitando o teste unitário e a manutenção do fluxo de trabalho assíncrono.
    """
    async def _generate_code_content(agent_name: str, topic: str, description: str, slug: str) -> str:
        # Simula a lógica complexa de chamada à API/Gemma
        await asyncio.sleep(0.1)
        return f"Generated code for {topic} based on description: {description} (Agent: {agent_name})"

    async def _process_input_for_gemma(topic: str, description: str) -> tuple[str, str]:
        # Simula a lógica de preparação dos prompts
        prompt = f"Synthesize code for topic: {topic}. Description: {description}"
        return prompt, slug

    async def call_gemma_for_code(agent_name: str, topic: str, description: str, slug: str) -> tuple[str, str]:
        """
        Função refatorada que orquestra a síntese de código.
        """
        prompt, slug_result = await _process_input_for_gemma(topic, description)
        generated_content = await _generate_code_content(agent_name, topic, description, slug_result)
        return generated_content, slug_result

# Importação necessária para o asyncio (assumido que o ambiente permite)
import asyncio