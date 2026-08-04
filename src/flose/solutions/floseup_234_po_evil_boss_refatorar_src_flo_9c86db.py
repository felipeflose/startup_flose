def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Modularizar a função de síntese de código para melhorar a performance assíncrona e a manutenibilidade do código, alinhando-se aos princípios de design de agentes.
    Visão Técnica AST: Refatorar a corotina 'call_gemma_for_code' (atualmente 76 linhas) em um módulo mais coeso, separando a lógica de chamada da API LLM da lógica de processamento de entrada e saída.
    """
    async def _call_gemma_api(agent_name: str, topic: str, description: str, slug: str) -> tuple[str, str]:
        """Simula a chamada assíncrona ao modelo de código."""
        # Lógica real de chamada à API/LLM deve residir aqui.
        # Para fins de teste, retornamos valores simulados.
        await asyncio.sleep(0.01)
        return "Generated Code Content", "Generated Slug"

    async def call_gemma_for_code(agent_name: str, topic: str, description: str, slug: str) -> tuple[str, str]:
        """
        Função refatorada que orquestra a síntese de código.
        """
        print(f"Starting code synthesis for agent: {agent_name}")
        
        # 1. Processamento da entrada (Lógica modularizada)
        processed_description = f"Agent: {agent_name}, Topic: {topic}. Request: {description}"
        
        # 2. Chamada ao módulo de API (Separação de responsabilidades)
        code_content, generated_slug = await _call_gemma_api(agent_name, topic, processed_description, slug)
        
        # 3. Formatação da saída
        result = (code_content, generated_slug)
        print("Code synthesis complete.")
        return result

# Import necessário para simular o ambiente assíncrono
import asyncio