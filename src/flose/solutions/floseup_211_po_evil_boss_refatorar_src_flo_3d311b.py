"""
Visão de Negócio: A função _do_real_commit é responsável por realizar um commit real em um sistema de controle de versão asynchronously. O objetivo é garantir que todas as operações sejam tipadas corretamente para melhorar a legibilidade e a segurança do código.

Visão Técnica AST: O script será utilizado para varrer e otimizar o código da função _do_real_commit em src/flose/web_app.py, adicionando anotações de tipo de retorno para melhorar a tipagem asynchronous.
"""

import ast
from typing import Optional

class AddReturnAnnotations(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        if node.name == "_do_real_commit":
            for arg in node.args.args:
                arg.annotation = ast.Name(id=arg.arg.replace('Key', 'KeyType'), ctx=ast.Load())
            return_type = ast.Name(id='Optional[str]', ctx=ast.Load())
            node.returns = return_type
        return self.generic_visit(node)

def add_return_annotations_to_file(file_path: str):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    transformer = AddReturnAnnotations()
    new_tree = transformer.visit(tree)

    with open(file_path, "w") as file:
        file.write(ast.unparse(new_tree))

if __name__ == "__main__":
    add_return_annotations_to_file("src/flose/web_app.py")