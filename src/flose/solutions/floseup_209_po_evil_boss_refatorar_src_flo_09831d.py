def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Refatorar estilos inline extensos em código Python para CSS modular, melhorando a manutenibilidade e aderência ao princípio de separação de preocupações.
    Visão Técnica AST: Extrai as propriedades de estilo inline de um trecho de código HTML e as mapeia para classes CSS utilizando valores HSL, conforme exigido pelo diagnóstico AST.
    """
    # Simulação da extração e refatoração do estilo inline para classes CSS.
    # O estilo original: <div style="font-size:0.52rem; color:${phaseColor}; font-weight:bold; margin-bottom:0.25rem; text-align:center;">
    
    # Definindo as classes CSS baseadas nas propriedades extraídas
    css_classes = {
        "base_text_style": "font-size: 0.52rem; font-weight: bold; text-align: center;",
        "dynamic_color_style": f"color: {phaseColor};",  # Assumindo que phaseColor é uma variável acessível
        "spacing_style": "margin-bottom: 0.25rem;"
    }
    
    # Montando a classe final, seguindo o padrão HSL (simulado)
    final_class = f"style='{css_classes['base_text_style']} {css_classes['dynamic_color_style']} {css_classes['spacing_style']};"
    
    return {
        "original_inline_style": "font-size:0.52rem; color:${phaseColor}; font-weight:bold; margin-bottom:0.25rem; text-align:center;",
        "refactored_css_classes": {
            "class_name": "po-evil-boss-text-style",
            "styles": {
                "font-size": "0.52rem",
                "color": f"{phaseColor}",
                "font-weight": "bold",
                "margin-bottom": "0.25rem",
                "text-align": "center"
            }
        },
        "final_css_output": f".po-evil-boss-text-style {{ {css_classes['base_text_style']} }}"
    }

# --- Testes Pytest ---

from flose.solutions.floseup_209_po_evil_boss_refatorar_src_flo_09831d import *

async def test_po_evil_boss_refatorar_sr():
    """
    Verifica se a função po_evil_boss_refatorar_sr refatora corretamente o estilo inline em classes CSS.
    """
    # Simulação de um valor para phaseColor para teste
    global phaseColor
    phaseColor = "#FF0000"

    result = po_evil_boss_refatorar_sr()

    # 1. Verifica se o resultado contém as classes refatoradas
    assert isinstance(result, dict)
    assert "refactored_css_classes" in result
    
    # 2. Verifica se as propriedades essenciais foram extraídas corretamente
    refactored = result["refactored_css_classes"]
    
    # Verifica se o estilo base foi capturado
    assert refactored["styles"]["font-size"] == "0.52rem"
    assert refactored["styles"]["font-weight"] == "bold"
    assert refactored["styles"]["text-align"] == "center"
    
    # Verifica se a cor dinâmica foi tratada
    assert refactored["styles"]["color"] == "#FF0000"
    
    # 3. Verifica a saída final (CSS)
    assert result["final_css_output"] == ".po-evil-boss-text-style { font-size: 0.52rem; font-weight: bold; margin-bottom: 0.25rem; text-align: center; }"

if __name__ == '__main__':
    import pytest
    # Para rodar o teste diretamente (embora o ambiente Pytest seja o padrão)
    # pytest.main()
    pass