from flose.solutions.floseup_234_po_evil_boss_refatorar_src_flo_9c86db import po_evil_boss_refatorar_sr

import pytest

# Configuração para rodar funções assíncronas em testes
def test_call_gemma_for_code_refactored():
    """
    Testa a função refatorada call_gemma_for_code, garantindo que ela execute
    a chamada modularizada corretamente.
    """
    async def run_test():
        agent_name = "CodeSynthAgent"
        topic = "Refactoring"
        description = "Implement the async call logic cleanly."
        slug = "refactor-request"
        
        # Executa a função refatorada
        result = await po_evil_boss_refatorar_sr(agent_name, topic, description, slug)
        
        # Validação básica do resultado esperado
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], str)
        
        # Verificação da lógica simulada
        assert result[0].startswith("Generated Code Content")
        assert result[1].startswith("Generated Slug")

    # Pytest requer que funções async sejam executadas com asyncio.run
    asyncio.run(run_test())

# Adicionando um teste de exemplo para garantir que a função existe
def test_refactoring_module_exists():
    """Verifica que o módulo e a função principal foram importados corretamente."""
    assert hasattr(po_evil_boss_refatorar_sr, '__call__')