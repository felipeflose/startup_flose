import ast

def po_evil_boss_refatorar_sr(source_code: str) -> str:
    """
    Visão de Negócio: Refatorar o estilo inline extenso em CSS modular usando classes HSL.
    Visão Técnica AST: Utiliza o módulo ast para analisar o código Python, identificando
    strings de estilo inline e sugerindo/aplicando a extração para classes CSS.
    """
    tree = ast.parse(source_code)
    new_lines = []
    style_found = False
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            # Check if the value is a string containing style attributes (simplified check)
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                value = node.value.value
                if 'style=' in value:
                    # Simulate the refactoring: extract style and replace it conceptually
                    # In a real scenario, this would involve complex string manipulation or AST node replacement.
                    
                    # Example transformation logic based on the specific example:
                    if 'color:' in value:
                        # Extract color value (e.g., '#a855f7')
                        color_value = value.split('color:')[1].split(';')[0].strip()
                        
                        # Simulate creating a modular class structure
                        css_class_name = f"style-color-{color_value.replace('#', '')}"
                        
                        # Replace the inline style attribute with a class reference
                        new_style_attr = f'class="{css_class_name}"'
                        
                        # Reconstruct the assignment node (highly simplified for demonstration)
                        # In a real scenario, we'd need to reconstruct the surrounding context.
                        new_node = ast.Assign(targets=node.targets, value=ast.Constant(value=new_style_attr))
                        new_lines.append(ast.unparse(new_node).strip())
                        style_found = True
                        continue
        
        # If no style was found, keep the original node
        new_lines.append(ast.unparse(node).strip())

    if not style_found:
        return source_code

    # Note: For a true refactoring, the output would be the modified source code string.
    # Since we are constrained to return a string result from the function, we return the processed lines.
    return "\n".join(new_lines)