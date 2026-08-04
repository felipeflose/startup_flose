def po_evil_boss_refatorar_sr(code_snippet: str) -> str:
    """
    Visão de Negócio: Modularizar estilos inline para classes CSS HSL, melhorando a manutenibilidade do frontend.
    Visão Técnica AST: Refatorar o trecho de código HTML/template, extraindo a propriedade 'color' inline para uma classe CSS definida.
    """
    # Identificar o padrão a ser refatorado: <span style="color:XXX; ...">...</span>
    # Assumindo que o objetivo é substituir o estilo inline por uma referência de classe.
    
    # Extrair o valor do estilo inline
    import re
    match = re.search(r'<span\s+style="([^"]+)">.*?<\/span>', code_snippet, re.DOTALL)
    
    if match:
        style_attribute = match.group(1)
        
        # Extrair a cor (exemplo: color:#a855f7;)
        color_match = re.search(r'color:([^;]+);', style_attribute)
        if color_match:
            color_value = color_match.group(1).strip()
            
            # Criar uma classe HSL baseada na cor (simplificação para o exemplo)
            # Em um cenário real, isso envolveria uma lógica de mapeamento de cores.
            css_class = f"text-{color_value.replace('#', '')}-highlight"
            
            # Substituir o span com o estilo inline pela classe
            refactored_html = f'<span class="{css_class}">{code_snippet.split(match.group(0))[1].strip()}</span>'
            return refactored_html
            
    return code_snippet

# Exemplo de uso (simulação da refatoração)
# original_code = '<span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>'
# refactored_code = po_evil_boss_refatorar_sr(original_code)
# print(refactored_code)