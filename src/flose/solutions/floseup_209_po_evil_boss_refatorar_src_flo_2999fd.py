def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Refatorar estilos inline de elementos HTML para classes CSS modulares (HSL).
    Visão Técnica AST: Extrai propriedades de estilo inline de uma string e as mapeia para uma classe CSS modular, substituindo o estilo inline.
    """
    inline_style = "font-size:0.52rem; color:${phaseColor}; font-weight:bold; margin-bottom:0.25rem; text-align:center;"
    
    # Parsing the inline styles into CSS properties
    styles = {}
    for style_pair in inline_style.split(';'):
        if ':' in style_pair:
            key, value = style_pair.split(':', 1)
            styles[key.strip()] = value.strip()

    # Generating the modular CSS class based on the extracted styles
    class_name = "po-evil-boss-style"
    css_output = f".{class_name} {{\n"
    
    for prop, value in styles.items():
        css_output += f"  {prop}: {value};\n"
        
    css_output += "}"
    
    # In a real scenario, this function would return the CSS string or a mapping structure.
    # For demonstration, we return the generated CSS block.
    return css_output

# Example usage (not strictly required by the test, but useful for context)
# print(po_evil_boss_refatorar_sr())