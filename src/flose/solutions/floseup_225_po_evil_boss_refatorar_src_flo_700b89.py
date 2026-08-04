def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Refatorar o estilo inline extenso em classes CSS modulares (HSL) para melhorar a manutenibilidade e a separação de responsabilidades do frontend.
    Visão Técnica AST: Substituir a aplicação de estilos inline no template de string por classes CSS pré-definidas.
    """
    def generate_css_classes(style_string: str) -> str:
        """Extrai estilos inline e os mapeia para classes HSL."""
        styles = {}
        if style_string:
            # Simplificação: extração baseada no exemplo fornecido.
            # Em um cenário real, isso exigiria uma análise mais robusta de CSS.
            if "font-size:0.38rem" in style_string:
                styles['font-size'] = '0.38rem'
            if "color:#ff5555" in style_string:
                styles['color'] = '#ff5555'
            if "margin-bottom:0.2rem" in style_string:
                styles['margin-bottom'] = '0.2rem'

        class_names = []
        if styles:
            # Mapeamento para classes HSL (exemplo)
            class_names.append(f'po-rejection-reason--{styles.get("font-size", "default")}')
            class_names.append(f'po-rejection-reason--{styles.get("color", "default")}')
            class_names.append(f'po-rejection-reason--{styles.get("margin-bottom", "default")}')
        
        return " ".join(class_names) if class_names else ""

    def refactor_template(template: str) -> str:
        """Refatora o template substituindo o estilo inline por classes."""
        if not template:
            return ""

        # Identifica o trecho a ser estilizado (o div)
        start_tag = template.find('<div')
        end_tag = template.find('</div')

        if start_tag == -1 or end_tag == -1:
            return template # Não encontrou o bloco a refatorar

        # Extrai o conteúdo do div (o texto)
        content = template[start_tag + 5 : end_tag] # Pula '<div'

        # Gera as classes CSS
        classes = generate_css_classes(template[start_tag:end_tag])

        # Reconstrói o HTML usando as classes
        new_div = f'<div class="{classes}">{content}</div>'

        # Substitui o bloco original pelo novo
        return template[:start_tag] + new_div + template[end_tag + 6:]

    # Simulação do código real a ser refatorado (baseado no exemplo)
    original_code = "${duel.active_card.po_rejection_reason ? `<div style=\"font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;\">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>` : ''}"

    # Aplica a refatoração
    refactored_code = refactor_template(original_code)
    
    return refactored_code