"""
Módulo de Solução para [FLOSEUP-106]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/agents/po_auditor.py: Backend/TratamentoErros (Linha 115)
Responsável: Sofia
"""

def handle_error(self, task_id, error):
    # Specific exceptions handling
    if isinstance(error, ValueError):
        self.logger.error(f"ValueError occurred for task {task_id}: {error}")
    elif isinstance(error, TypeError):
        self.logger.error(f"TypeError occurred for task {task_id}: {error}")
    else:
        # Generic exception handling
        self.logger.error(f"An unexpected error occurred for task {task_id}: {error}")

# Test function for the handle_error method
def test_handle_error(mocker):
    po_auditor = POAuditor()
    po_auditor.logger = mocker.patch('src.flose.agents.po_auditor.Logger')

    # Simulate a ValueError
    with pytest.raises(ValueError):
        raise ValueError("Invalid value")
    po_auditor.handle_error(123, ValueError("Invalid value"))
    po_auditor.logger.error.assert_called_once_with('ValueError occurred for task 123: Invalid value')

    # Simulate a TypeError
    with pytest.raises(TypeError):
        raise TypeError("Type error")
    po_auditor.handle_error(456, TypeError("Type error"))
    po_auditor.logger.error.assert_called_once_with('TypeError occurred for task 456: Type error')

    # Simulate a generic exception
    with pytest.raises(Exception):
        raise Exception("Generic error")
    po_auditor.handle_error(789, Exception("Generic error"))
    po_auditor.logger.error.assert_called_once_with('An unexpected error occurred for task 789: Generic error')