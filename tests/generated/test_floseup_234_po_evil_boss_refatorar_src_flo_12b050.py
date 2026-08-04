from flose.solutions.floseup_234_po_evil_boss_refatorar_src_flo_12b050 import *

import pytest

# Mock para simular o ambiente, pois não temos acesso ao código real do sistema
# Em um ambiente real, estas dependências seriam injetadas ou mockadas de forma mais robusta.
class MockModule:
    pass

# O código refatorado deve ser importado e testado
# Assumindo que a função po_evil_boss_refatorar_sr está acessível via import
# Para fins de teste, redefinimos o contexto necessário (o código acima é a implementação)

# Teste da função refatorada
def test_refactored_code_synthesis():
    # Teste a função principal refatorada
    agent_name = "Gemma4"
    topic = "Python Refactoring"
    description = "Modularize o código de síntese."
    slug = "refactor_task"

    # Executa a função assíncrona
    result = asyncio.run(po_evil_boss_refatorar_sr(agent_name, topic, description, slug))

    # Verificação básica da estrutura do resultado
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], str)
    
    # Verificação da lógica de saída simulada
    assert "Code fetched" in result[0]
    assert "Synthesized content" in result[1]