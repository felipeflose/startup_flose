import ast

class ASTOptimizer(ast.NodeTransformer):
    def visit_While(self, node):
        # Simplify if-while structures where the condition is always False or True
        if isinstance(node.test, (ast.Constant, ast.Compare)):
            return node.body
        return super().visit_While(node)

def optimize_python_code(code):
    tree = ast.parse(code)
    optimized_tree = ASTOptimizer().visit(tree)
    return compile(optimized_tree, filename="<ast>", mode="exec")

# Example usage:
code = """
while True:
    if condition:
        break
"""
optimized_code = optimize_python_code(code)
print(optimized_code)