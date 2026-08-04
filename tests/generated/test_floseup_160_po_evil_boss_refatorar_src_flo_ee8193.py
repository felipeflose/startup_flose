from flose.solutions.floseup_160_po_evil_boss_refatorar_src_flo_ee8193 import *
import pytest
from unittest.mock import patch

# Testando a função refatorada
def test_po_evil_boss_refatorar_sr():
    # Configuração para mockar o logger
    with patch('floseup_160_po_evil_boss_refatorar_src_flo_ee8193.logging.getLogger') as mock_get_logger:
        mock_logger = mock_get_logger.return_value
        
        # Teste 1: Exceção genérica (simulando Exception)
        exception_generic = Exception("Something went terribly wrong")
        result_generic = po_evil_boss_refatorar_sr(exception_generic)
        
        # Espera que o logger tenha sido chamado com um erro (nível ERROR)
        mock_logger.error.assert_called_once()
        assert result_generic.get("error") == "Internal Server Error"

        # Teste 2: Exceção específica (simulando um erro de validação, ex: ValueError)
        exception_specific = ValueError("Invalid input data")
        result_specific = po_evil_boss_refatorar_sr(exception_specific)
        
        # Espera que o logger tenha sido chamado com um aviso (nível WARNING)
        mock_logger.warning.assert_called_once()
        assert result_specific.get("error") == "Operation failed: ValueError"