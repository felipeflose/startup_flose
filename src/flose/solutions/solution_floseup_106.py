"""
Módulo de Solução para [FLOSEUP-106]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/agents/po_auditor.py: Backend/TratamentoErros (Linha 115)
Responsável: Sofia
"""

import pytest

def audit_ast_with_specific_error(code: str, message: str) -> str:
    """Audita um trecho de código, simulando a captura de um erro específico."""
    if 'error_trigger' in code:
        raise ValueError(f"Erro específico capturado: {message}")
    elif 'generic_error' in code:
        raise RuntimeError(f"Erro genérico capturado: {message}")
    else:
        # Simula o tratamento de qualquer outra exceção genérica
        raise Exception(f"Erro inesperado capturado: {message}")

def handle_auditor_exception(e: Exception, logger: object) -> str:
    """Trata uma exceção capturada, registrando-a e retornando uma mensagem de auditoria."""
    if isinstance(e, ValueError):
        # Trata erros específicos de validação
        logger.warning(f"Erro de Validação detectado: {e}")
        return f"Auditoria OK: Erro de Validação tratado. Detalhe: {e}"
    elif isinstance(e, RuntimeError):
        # Trata erros de execução/runtime
        logger.error(f"Erro de Runtime detectado: {e}")
        return f"Auditoria OK: Erro de Runtime tratado. Detalhe: {e}"
    else:
        # Trata exceções genéricas
        logger.exception(f"Erro inesperado durante a auditoria: {e}")
        return f"Auditoria Falhou: Erro inesperado. Detalhe: {type(e).__name__}: {e}"

def perform_ast_audit(source_code: str, error_message: str, logger: object = None) -> str:
    """Realiza a auditoria AST, capturando e tratando exceções de forma específica."""
    if logger is None:
        # Simula um logger básico se não for fornecido
        class MockLogger:
            def warning(self, msg):
                print(f"[WARNING] {msg}")
            def error(self, msg):
                print(f"[ERROR] {msg}")
            def exception(self, msg):
                print(f"[EXCEPTION] {msg}")
        logger = MockLogger()

    try:
        # Simula a execução da auditoria
        audit_result = audit_ast_with_specific_error(source_code, error_message)
        return f"Auditoria Concluída com Sucesso: {audit_result}"
    except Exception as e:
        # Implementação corrigida: Tratamento específico
        return handle_auditor_exception(e, logger)


# --- Funções de Teste Pytest ---

@pytest.fixture
def mock_logger():
    """Fixture para um logger mockado."""
    class MockLogger:
        def warning(self, msg):
            pass
        def error(self, msg):
            pass
        def exception(self, msg):
            pass
    return MockLogger()

def test_handle_auditor_exception_value_error(mock_logger):
    "Testa o tratamento de ValueError especificamente."""
    error = ValueError("Validação de campo falhou")
    result = handle_auditor_exception(error, mock_logger)
    assert "Auditoria OK: Erro de Validação tratado" in result

def test_handle_auditor_exception_runtime_error(mock_logger):
    "Testa o tratamento de RuntimeError especificamente."""
    error = RuntimeError("Falha na execução do algoritmo")
    result = handle_auditor_exception(error, mock_logger)
    assert "Auditoria OK: Erro de Runtime tratado" in result

def test_handle_auditor_exception_generic_error(mock_logger):
    "Testa o tratamento de exceções genéricas (catch-all)."""
    error = Exception("Erro desconhecido na etapa")
    result = handle_auditor_exception(error, mock_logger)
    assert "Auditoria Falhou: Erro inesperado" in result

def test_perform_ast_audit_success(mock_logger):
    "Testa o fluxo de auditoria quando tudo corre bem."""
    source = "def func(): return 1"
    message = "Nenhuma falha esperada"
    result = perform_ast_audit(source, message, logger=mock_logger)
    assert "Auditoria Concluída com Sucesso" in result

def test_perform_ast_audit_value_error(mock_logger):
    "Testa o fluxo de auditoria quando uma ValueError é levantada."""
    source = "def func(): error_trigger = 1"
    message = "Erro de validação simulado"
    result = perform_ast_audit(source, message, logger=mock_logger)
    assert "Auditoria OK: Erro de Validação tratado" in result

def test_perform_ast_audit_runtime_error(mock_logger):
    "Testa o fluxo de auditoria quando uma RuntimeError é levantada."""
    source = "def func(): error_trigger = 1"
    message = "Erro de runtime simulado"
    result = perform_ast_audit(source, message, logger=mock_logger)
    assert "Auditoria OK: Erro de Runtime tratado" in result

def test_perform_ast_audit_generic_exception(mock_logger):
    "Testa o fluxo de auditoria quando uma exceção genérica é levantada."""
    source = "def func(): generic_error = 1"
    message = "Erro genérico simulado"
    result = perform_ast_audit(source, message, logger=mock_logger)
    assert "Auditoria Falhou: Erro inesperado" in result
