from flose.solutions.floseup_237_pico_ast_refactoring_stage_1_1104f2 import *

def test_pico_ast_refactoring_stag():
    """
    Testa a função pico_ast_refactoring_stag com um código de exemplo.
    """
    source_code = """
def calculate_sum(a, b):
    return a + b

def process_data(data):
    result = sum(data)
    return result
"""

    result = pico_ast_refactoring_stag(source_code)

    # Verificação básica para garantir que a função foi chamada e processada
    assert "Function found: calculate_sum" in result
    assert "Function found: process_data" in result
    assert "Refatorado: Função 'calculate_sum' foi comentada." in result
    assert "Refatorado: Função 'process_data' foi comentada." in result

if __name__ == '__main__':
    test_pico_ast_refactoring_stag()