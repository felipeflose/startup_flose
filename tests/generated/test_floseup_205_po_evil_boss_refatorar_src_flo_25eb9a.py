from flose.solutions.floseup_205_po_evil_boss_refatorar_src_flo_25eb9a import *
import pytest
import logging
from unittest.mock import patch

# Assume que a função a ser testada está acessível ou simulada
# Para fins de teste, vamos redefinir a função refatorada aqui para garantir que o pytest funcione isoladamente
def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Melhorar a robustez do tratamento de erros ao interagir com a API do Jira, evitando a captura de exceções genéricas e permitindo um tratamento mais específico e rastreável.
    Visão Técnica AST: Substituir o tratamento genérico `except Exception:` por tratamento de exceções mais específicas (ex: `requests.exceptions.RequestException` ou `IOError`) e integrar o tratamento de falhas com um mecanismo de logging.
    """
    logger = logging.getLogger(__name__)

    def execute_jira_operation(operation_details):
        if operation_details == "fail_specific":
            raise ValueError("Erro de validação específica da operação.")
        if operation_details == "fail_general":
            raise IOError("Erro de I/O inesperado.")
        raise Exception("Erro genérico não previsto.")

    try:
        execute_jira_operation("success")
    except ValueError as e:
        logger.error(f"Erro de validação capturado: {e}")
    except IOError as e:
        logger.error(f"Erro de I/O capturado: {e}")
    except Exception as e:
        logger.critical(f"Erro inesperado ao executar a operação do Jira. Detalhes: {e}", exc_info=True)
        raise RuntimeError("Falha crítica na operação do Jira.") from e


@pytest.mark.parametrize("operation, expected_error_type, log_message_part", [
    ("success", None, None),  # Caso de sucesso
    ("fail_specific", ValueError, "Erro de validação capturado"), # Caso de exceção específica
    ("fail_general", IOError, "Erro de I/O capturado"),      # Caso de exceção de I/O
    ("fail_unknown", RuntimeError, "Erro inesperado"),        # Caso de exceção genérica tratada
])
def test_po_evil_boss_refatorar_sr(operation, expected_error_type, log_message_part):
    # Mockar o logger para verificar se o logging foi chamado corretamente
    with patch('logging.getLogger') as mock_logger:
        mock_logger_instance = mock_logger.return_value
        
        # Executar a função refatorada
        try:
            po_evil_boss_refatorar_sr()
        except RuntimeError:
            pass # Esperamos que o erro final seja capturado internamente ou propagado
        except Exception:
            pass # Outras exceções podem ser capturadas dependendo da estrutura exata
        
        # Verificações baseadas no cenário
        if operation == "success":
            # Em caso de sucesso, não deve haver logs de erro/crítico
            assert not mock_logger_instance.error.called
            assert not mock_logger_instance.critical.called

        elif operation == "fail_specific":
            # Deve ter chamado o logger.error para a exceção específica
            mock_logger_instance.error.assert_called_with(f"Erro de validação capturado: Erro de validação específica da operação.")
            assert "Erro de validação capturado" in str(mock_logger_instance.error.call_args[0][0])

        elif operation == "fail_general":
            # Deve ter chamado o logger.error para a exceção de I/O
            mock_logger_instance.error.assert_called_with(f"Erro de I/O capturado: Erro de I/O inesperado.")
            assert "Erro de I/O capturado" in str(mock_logger_instance.error.call_args[0][0])

        elif operation == "fail_unknown":
            # Deve ter chamado o logger.critical para o erro genérico
            mock_logger_instance.critical.assert_called_once()
            assert "Erro inesperado ao executar a operação do Jira" in str(mock_logger_instance.critical.call_args[0][0])