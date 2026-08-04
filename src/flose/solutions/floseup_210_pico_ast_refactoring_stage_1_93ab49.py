"""
Visão de Negócio: A otimização da AST é crucial para melhorar o desempenho e a eficiência do código Python, reduzindo custos computacionais e aumentando a produtividade.

Visão Técnica AST: Esta função realiza uma análise sintática e estrutural do código Python representado como uma Árvore de Sintaxe Abstrata (AST). Ela identifica padrões comuns e aplica otimizações para reduzir a complexidade e melhorar o desempenho.
"""

import ast
from collections import defaultdict

class ASTOptimizer(ast.NodeTransformer):
    def __init__(self):
        self.stats = defaultdict(int)
    
    def visit_BinOp(self, node):
        # Exemplo de otimização: (a + 0) -> a
        if isinstance(node.right, ast.Num) and node.right.n == 0:
            return node.left
        # Exemplo de otimização: (a * 1) -> a
        elif isinstance(node.right, ast.Num) and node.right.n == 1:
            return node.left
        self.stats[type(node).__name__] += 1
        return self.generic_visit(node)
    
    def visit_Call(self, node):
        # Exemplo de otimização: print("Hello", end=" ") -> print("Hello")
        if isinstance(node.func.id, str) and node.func.id == "print":
            args = [arg for arg in node.args if not isinstance(arg, ast.keyword)]
            if len(args) > 1:
                node.args = args
                node.keywords = []
        self.stats[type(node).__name__] += 1
        return self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        # Exemplo de otimização: def foo(x): return x -> def foo(x): x
        if len(node.body) == 1 and isinstance(node.body[0], ast.Return):
            node.body = [node.body[0].value]
        self.stats[type(node).__name__] += 1
        return self.generic_visit(node)
    
    def get_stats(self):
        return dict(self.stats)

def optimize_ast(code):
    tree = ast.parse(code)
    optimizer = ASTOptimizer()
    optimized_tree = optimizer.visit(tree)
    stats = optimizer.get_stats()
    return optimized_tree, stats

# Exemplo de uso
if __name__ == "__main__":
    code = """
def add(a, b):
    return a + 0

def greet():
    print("Hello", end=" ")

def foo(x):
    return x
"""
    optimized_code, stats = optimize_ast(code)
    print(ast.unparse(optimized_code))
    print(stats)