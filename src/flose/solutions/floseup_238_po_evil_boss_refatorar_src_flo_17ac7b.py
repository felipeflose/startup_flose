import ast
import re
from typing import Union

def po_evil_boss_refatorar_sr(code_snippet: str) -> str:
    """
    Visão de Negócio: Migrar estilos inline de elementos HTML para classes CSS modulares baseadas em HSL.
    Visão Técnica AST: Auditoria e refatoração de código Python que manipula strings HTML para extrair e reestruturar estilos inline em classes CSS.
    """
    # Regex para encontrar a tag <span> com estilo inline
    # Exemplo: <span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>
    match = re.search(r'<span\s+style\s="([^"]+)">(.+?)<\/span>', code_snippet, re.DOTALL)

    if not match:
        return code_snippet

    style_attribute = match.group(1)
    content = match.group(2).strip()

    # Extrair estilos
    styles = {}
    style_parts = style_attribute.split(';')
    for part in style_parts:
        if ':' in part:
            key, value = part.split(':', 1)
            styles[key.strip()] = value.strip()

    # Refatorar os estilos para classes HSL
    # Assumindo que a cor principal é 'color' e a propriedade 'float' é tratada separadamente.
    color = styles.get('color', '#000000')
    float_style = styles.get('float', '')

    # Criar uma classe base com a cor HSL
    css_class = f"style=\"color:hsl({int(color.lstrip('#') * 255)}, {int(color[1:3]) * 255}, {int(color[3:5]) * 255}); float:{float_style};\""

    # Reconstruir o trecho HTML com a classe
    refactored_snippet = f'<span class="{css_class}">{content}</span>'

    return refactored_snippet

# Exemplo de uso simulado (simulando o trecho da linha 1616)
test_input = '<span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>'
refactored_output = po_evil_boss_refatorar_sr(test_input)
# print(refactored_output)