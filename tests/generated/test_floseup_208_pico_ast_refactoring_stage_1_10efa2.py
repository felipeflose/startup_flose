from flose.solutions.floseup_208_pico_ast_refactoring_stage_1_10efa2 import *

import ast
import sys

def test_pico_ast_refactoring_stag():
    """
    Testa a função pico_ast_refactoring_stag com um AST de exemplo.
    """
    # 1. Criar um AST de teste que contenha um nome a ser refatorado
    code_to_test = "old_var = 10\nresult = old_var + 5"
    tree = ast.parse(code_to_test)

    # 2. Executar a função a ser testada
    refactored_tree = pico_ast_refactoring_stag(tree)

    # 3. Verificar o resultado
    
    # Procurar pelo nó de atribuição (Assign)
    for node in ast.walk(refactored_tree):
        if isinstance(node, ast.Assign):
            print(f"Verificando atribuição: {ast.dump(node)}")
            
            # Verificar se o nome 'old_var' foi renomeado para 'new_refactored_var'
            if len(node.targets) > 0 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'new_refactored_var':
                print("SUCESSO: O nome da variável foi refatorado corretamente.")
                return

    print("FALHA: A refatoração não foi detectada no AST de teste.")
    sys.exit(1)

if __name__ == '__main__':
    test_pico_ast_refactoring_stag()