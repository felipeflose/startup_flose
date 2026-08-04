# flose/solutions/floseup_190_pico_ast_refactoring_stage_44_b37b4a.py

import ast

def refactor_code(code: str) -> str:
    tree = ast.parse(code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            node.decorator_list.append(ast.Name(id='deprecated', ctx=ast.Load()))
    
    return ast.unparse(tree)

# Exemplo de uso
if __name__ == "__main__":
    code = """
def old_function():
    print("Hello, World!")
"""
    refactored_code = refactor_code(code)
    print(refactored_code)