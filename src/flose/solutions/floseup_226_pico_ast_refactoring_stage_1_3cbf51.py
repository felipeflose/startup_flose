"""
Visão de Negócio: Refatorar código Python usando AST para aumentar a eficiência e legibilidade.
Visão Técnica AST: Utilizar o módulo `ast` para analisar, manipular e otimizar a estrutura de árvore abstrata do código Python.
"""

import ast
from collections import defaultdict

class ASTRefactoringVisitor(ast.NodeTransformer):
    def __init__(self):
        self.variable_usage = defaultdict(int)
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.variable_usage[node.id] += 1
        return super().visit_Name(node)
    
    def leave_FunctionDef(self, node):
        # Optimize function calls that reuse variables
        for stmt in node.body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                func_name = stmt.value.func.id
                args = [arg.id for arg in stmt.value.args]
                if all(arg in self.variable_usage for arg in args):
                    # Replace function call with a simple variable reference
                    node.body[stmt] = ast.Assign(targets=[ast.Name(id=func_name, ctx=ast.Store())],
                                                  value=ast.Call(func=ast.Name(id=func_name, ctx=ast.Load()),
                                                                  args=[ast.Name(id=arg, ctx=ast.Load()) for arg in args],
                                                                  keywords=[]))
        return super().leave_FunctionDef(node)

def optimize_code(code):
    tree = ast.parse(code)
    refactored_tree = ASTRefactoringVisitor().visit(tree)
    return compile(refactored_tree, filename="<ast>", mode="exec")

# Example usage
if __name__ == "__main__":
    code = """
def calculate(a, b, c):
    x = a + b
    y = b * c
    z = x + y
    return z

result = calculate(10, 20, 30)
print(result)
"""
    optimized_code = optimize_code(code)
    exec(optimized_code)