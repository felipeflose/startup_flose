def po_evil_boss_refatorar_sr(duel_data: dict) -> str:
    """
    Visão de Negócio: Refatorar estilos inline em CSS modular com classes HSL para melhorar a manutenibilidade e aderência ao sistema de design.
    Visão Técnica AST: Extrai atributos de estilo inline de um trecho de código dinâmico e os mapeia para classes CSS baseadas em HSL.
    """
    
    # Extrair os estilos inline do trecho original (simulação da extração do AST)
    # Estilos a serem extraídos: font-size:0.38rem, color:#ff5555, margin-bottom:0.2rem
    
    # Mapeamento dos estilos para classes HSL
    base_style_class = "style-po-rejection-reason"
    
    # Determinar as classes baseadas nos estilos extraídos
    # font-size:0.38rem -> font-size-sm
    # color:#ff5555 -> color-error-5555
    # margin-bottom:0.2rem -> mb-sm
    
    dynamic_content = ""
    if duel_data.get('active_card', {}).get('po_rejection_reason'):
        rejection_reason = duel_data['active_card']['po_rejection_reason'].substring(0, 50)
        dynamic_content = f"💬 {rejection_reason}"

    # Construir o HTML usando classes HSL
    if dynamic_content:
        # Aplicação das classes HSL
        html_output = f'<div class="{base_style_class} font-size-sm color-error-5555 mb-sm">{dynamic_content}</div>'
    else:
        html_output = ""
        
    return html_output