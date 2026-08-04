import ast
from cssutils import parseString
import re

def refactor_web_app(py_file_path):
    with open(py_file_path, 'r') as file:
        code = file.read()

    tree = ast.parse(code)

    # Define a regex para encontrar estilos inline extensos
    style_regex = re.compile(r'style="([^"]+)"')

    class CSSRefactor(ast.NodeTransformer):
        def visit_Jinja2Template(self, node):
            for item in node.items:
                if isinstance(item, ast.Expr) and isinstance(item.value, ast.Str):
                    match = style_regex.search(item.value.s)
                    if match:
                        styles = parseString(match.group(1))
                        css_classes = []
                        for rule in styles.cssRules:
                            class_name = f'custom_{rule.selectorText.strip().replace(".", "")}'
                            node.items.append(ast.Expr(value=ast.Str(f'<style>.{class_name}{{{rule.cssText}}}</style>')))
                            css_classes.append(class_name)
                        new_value = re.sub(style_regex, f'class="{{ " ".join(css_classes) }}"', item.value.s)
                        node.items.append(ast.Expr(value=ast.Str(new_value)))
            return self.generic_visit(node)

    refactored_tree = CSSRefactor().visit(tree)
    refactored_code = ast.unparse(refactored_tree)

    with open(py_file_path, 'w') as file:
        file.write(refactored_code)


# Use a função para refatorar o arquivo web_app.py
refactor_web_app('src/flose/web_app.py')