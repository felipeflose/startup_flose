def po_evil_boss_refatorar_sr(code_snippet: str) -> str:
    """
    Visão de Negócio: Refatorar estilos inline de elementos HTML para classes CSS modulares HSL.
    Visão Técnica AST: Extrai o estilo inline de um trecho de código Python/HTML e o mapeia para classes CSS baseadas em HSL.
    """
    # Simulação da extração do trecho de código
    # O código original é: <span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>
    
    # 1. Identificar o estilo inline
    style_attribute = ""
    text_content = code_snippet
    
    if 'style=' in code_snippet:
        start_tag = code_snippet.find('<span style=') + len('<span style=')
        end_tag = code_snippet.find('>', start_tag)
        style_attribute = code_snippet[start_tag:end_tag]
        
        # Remover o estilo do texto para obter o conteúdo puro
        text_content = code_snippet[:start_tag] + code_snippet[end_tag:]

    # 2. Extrair cores e propriedades (simulação baseada no exemplo)
    # Neste cenário, extraímos apenas a cor HSL: color:#a855f7
    
    if style_attribute:
        # Simplificação: extrair apenas a cor para criar uma classe HSL
        try:
            color_hex = style_attribute.split(';')[0].strip()
            # Assumindo que o formato é 'color:#a855f7'
            if color_hex.startswith('color:'):
                hsl_value = color_hex.split(':')[1].strip()
                # Criar uma classe CSS modular
                css_class = f"style-hsl-{hsl_value}"
            else:
                css_class = "style-default"
        except Exception:
            css_class = "style-error"
    else:
        css_class = "style-default"

    # 3. Reconstruir o trecho com a classe CSS aplicada
    refactored_html = f'<span class="{css_class}">{text_content}</span>'
    
    return refactored_html

if __name__ == '__main__':
    # Teste de exemplo
    input_code = '<span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>'
    output_code = po_evil_boss_refatorar_sr(input_code)
    print(f"Original: {input_code}")
    print(f"Refatorado: {output_code}")