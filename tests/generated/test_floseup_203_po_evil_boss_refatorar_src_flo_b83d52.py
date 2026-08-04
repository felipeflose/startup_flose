"""
Testes para a solução de adicionar tipo de retorno à função async 'background_boss_card_generator'
"""

import pytest
from flose.solutions.floseup_203_po_evil_boss_refatorar_src_flo_b83d52 import optimize_code_with_ast

def test_add_return_type_to_async_function():
    source_code = """
    async def background_boss_card_generator():
        pass
    """
    optimized_code = optimize_code_with_ast(source_code, 'dict')
    
    tree = ast.parse(optimized_code.co_code.decode())
    found_return_type = None
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) and node.name == 'background_boss_card_generator':
            found_return_type = node.returns
    
    assert found_return_type is not None, "Return type should be added to the async function"
    assert isinstance(found_return_type, ast.NameConstant), "Return type should be a NameConstant"
    assert found_return_type.value.id == 'dict', "Return type should be 'dict'"

if __name__ == "__main__":
    pytest.main()