"""
Visão de Negócio: O objetivo deste épico é refatorar o código-fonte do projeto FLOSEUP, focando na otimização da estrutura de árvore abstrata (AST) para melhorar a eficiência e legibilidade.

Visão Técnica AST: Este script utiliza a biblioteca `ast` para analisar e manipular a AST de um código Python. A ideia é identificar padrões que podem ser otimizados, como loops desnecessários, operações redundantes e outras melhorias estruturais.
"""

import ast
import astor

class CodeOptimizer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()

    def visit_For(self, node):
        # Remove loop body if it is a single expression that does nothing
        if isinstance(node.body, list) and len(node.body) == 1:
            stmt = node.body[0]
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Pass):
                return None

        return self.generic_visit(node)

    def visit_Assign(self, node):
        # Simplify assignments to constants
        if isinstance(node.value, ast.Num) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                return ast.Assign(targets=[target], value=node.value)

        return self.generic_visit(node)

    def visit_BinOp(self, node):
        # Combine addition of constants
        if isinstance(node.left, ast.Num) and isinstance(node.right, ast.Num):
            if isinstance(node.op, (ast.Add, ast.Mult)):
                return ast.BinOp(left=node.left, op=ast.Add(), right=node.right)

        return self.generic_visit(node)

    def visit_If(self, node):
        # Simplify if statements with constant conditions
        if isinstance(node.test, ast.Compare) and len(node.test.ops) == 1:
            op = node.test.ops[0]
            left = node.test.left
            right = node.test.comparators[0]

            if isinstance(op, (ast.Eq, ast.NotEq)):
                if isinstance(left, ast.NameConstant) and isinstance(right, ast.NameConstant):
                    return None

        return self.generic_visit(node)

def optimize_code(code):
    tree = ast.parse(code)
    optimized_tree = CodeOptimizer().visit(tree)
    optimized_code = astor.to_source(optimized_tree)
    return optimized_code