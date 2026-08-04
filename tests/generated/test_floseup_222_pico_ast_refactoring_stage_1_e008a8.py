from flose.solutions.floseup_222_pico_ast_refactoring_stage_1_e008a8 import *

def test_pico_ast_refactoring_stag():
    """
    Testa a função pico_ast_refactoring_stag com um código de exemplo.
    """
    test_code = """
def calculate(a, b):
    result = a + b
    return result
"""
    expected_refactoring = """
--- Refatorado via pico_ast_refactoring_stag ---
def calculate(a, b):
    result = a + b
    return result
"""
    actual_refactoring = pico_ast_refactoring_stag(test_code)
    
    assert actual_refactoring == expected_refactoring, "A refatoração do código não corresponde ao esperado."
    print("Teste pico_ast_refactoring_stag concluído com sucesso.")

if __name__ == "__main__":
    test_pico_ast_refactoring_stag()