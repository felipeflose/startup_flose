import pytest
from flose.solutions.floseup_221_po_evil_boss_refatorar_src_flo_6f2b6e import po_evil_boss_refatorar_sr

@pytest.fixture
def sample_code():
    """Fornece um trecho de código simulado para teste."""
    return "async def async_create_jira_card_background(topic_title: str, topic_desc: str):"

async def test_po_evil_boss_refatorar_sr():
    """Verifica se a função de refatoração aplica a documentação corretamente."""
    
    # Código de entrada simulado
    source_code = "async def async_create_jira_card_background(topic_title: str, topic_desc: str):"
    
    # Executar a refatoração
    result = po_evil_boss_refatorar_sr(source_code)
    
    # Verificação da presença da docstring esperada
    expected_start = """
    \"\"\"
    Cria um card do Jira em segundo plano.

    Esta função é responsável por iniciar o processo de criação de um card no Jira de forma assíncrona,
    executando operações de I/O fora do fluxo principal da aplicação.

    Args:
        topic_title: O título do card do Jira a ser criado.
        topic_desc: A descrição detalhada do card do Jira.
    \"\"\"
    async def async_create_jira_card_background(topic_title: str, topic_desc: str):"""
    
    assert expected_start in result
    assert "async def async_create_jira_card_background" in result
    
    print("Refatoração realizada com sucesso: Documentação adicionada.")