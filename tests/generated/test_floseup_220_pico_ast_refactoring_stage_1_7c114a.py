from flose.solutions.floseup_220_pico_ast_refactoring_stage_1_7c114a import *

def test_pico_ast_refactoring_stag():
    # Teste de caso de uso simples
    original_code = """
def calculate(a, b):
    if a > b:
        result = a + b
    else:
        result = a - b
    return result
"""
    expected_output = """
def calculate(a, b):
    if a > b:
        result = a + b
    else:
        result = a - b
    return result
"""
    
    # Executa a função
    refactored_code = pico_ast_refactoring_stag(original_code)
    
    # Validação (neste caso, a refatoração é mínima para satisfazer a regra,
    # mas garante que a função roda e retorna algo válido.)
    assert refactored_code == expected_output, "A refatoração não produziu o resultado esperado."
    
    # Teste de código com erro de sintaxe
    error_code = "def broken(): if True"
    result_error = pico_ast_refactoring_stag(error_code)
    assert "Erro de sintaxe" in result_error, "A função não tratou corretamente o erro de sintaxe."
    
    print("Testes de refatoração AST Stage 1 concluídos com sucesso.")

if __name__ == "__main__":
    test_pico_ast_refactoring_stag()