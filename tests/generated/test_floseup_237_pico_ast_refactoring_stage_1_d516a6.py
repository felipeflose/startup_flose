from flose.solutions.floseup_237_pico_ast_refactoring_stage_1_d516a6 import *

import pytest
import ast

def test_pico_ast_refactoring_stag_basic():
    """
    Testa se a função pico_ast_refactoring_stag manipula corretamente um nó AST básico.
    """
    # 1. Criar um nó de teste (Exemplo: uma expressão binária simples)
    left_val = ast.Constant(value=10)
    right_val = ast.Constant(value=5)
    
    original_node = ast.BinOp(left=left_val, op=ast.Add(), right=right_val)
    
    # 2. Executar a função a ser testada
    refactored_node = pico_ast_refactoring_stag(original_node)
    
    # 3. Assertivas
    # Garantir que o nó foi retornado
    assert refactored_node is original_node
    
    # Garantir que a estrutura do nó não foi alterada (simulação de que a refatoração
    # estágio 1 é preservativa, focando na estrutura AST)
    assert isinstance(refactored_node, ast.BinOp)
    assert refactored_node.op == ast.Add()
    assert refactored_node.left is left_val
    assert refactored_node.right is right_val

    # Testar um caso vazio/simples
    empty_node = ast.Name(id='x')
    refactored_empty = pico_ast_refactoring_stag(empty_node)
    assert refactored_empty is empty_node