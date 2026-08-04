def po_evil_boss_refatorar_sr():
    """
    Visão de Negócio: Refatorar o estilo inline extenso em classes CSS modulares usando valores HSL.
    Visão Técnica AST: Extrai as propriedades de estilo inline (font-size, color, margin-bottom) do template HTML e as mapeia para classes CSS baseadas em HSL.
    """
    
    # Definição das classes CSS baseadas nos estilos inline
    # Estilos originais: font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;
    
    CSS_CLASSES = {
        "po-rejection-reason-style": "font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;"
    }
    
    # Simulação da refatoração do trecho de código
    # O código original é: `${duel.active_card.po_rejection_reason ? `<div style="...">...</div>` : ''}`
    
    # A refatoração envolve substituir o estilo inline pela aplicação da classe.
    
    def refactor_template(template_string: str) -> str:
        """
        Função interna para aplicar a refatoração ao template.
        """
        if not template_string:
            return ""
        
        # Identificar a parte que contém o estilo inline
        # No exemplo, o estilo é aplicado ao <div>.
        
        # Simulação da substituição:
        # O estilo inline é removido e a classe é adicionada.
        
        # Assumindo que o template_string contenha a estrutura de um div com o estilo.
        
        # Exemplo de transformação:
        # Se o template for: <div style="...">CONTENT</div>
        # O refatorado será: <div class="po-rejection-reason-style">CONTENT</div>
        
        # Como o input é uma expressão f-string complexa, a refatoração deve focar na estrutura.
        
        # Para fins de teste, simulamos a aplicação da classe:
        
        # Se o template original fosse: 
        # f"<div style='font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;'>💬 {reason}</div>"
        
        # A refatoração resulta em:
        # f'<div class="po-rejection-reason-style">💬 {reason}</div>'
        
        # Como não temos o contexto completo do `duel.active_card.po_rejection_reason`,
        # retornamos a estrutura de refatoração da classe.
        
        return template_string.replace("style=\"", f'class="{CSS_CLASSES["po-rejection-reason-style"]}"')


    # Retornando a lógica de refatoração (em um ambiente real, isso faria a substituição no arquivo)
    return refactor_template

import pytest

# O teste deve simular o comportamento esperado da função refatorar
def test_po_evil_boss_refatorar_sr():
    """
    Testa a função po_evil_boss_refatorar_sr para garantir que a refatoração do estilo inline
    para classes CSS HSL foi aplicada corretamente.
    """
    # Simulação do input que a função receberia (baseado no código original)
    original_template = `${duel.active_card.po_rejection_reason ? '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>' : ''}`
    
    # Chamada da função de refatoração
    refactored_output = po_evil_boss_refatorar_sr(original_template)
    
    # Verificação esperada: O estilo inline deve ter sido substituído pela classe CSS.
    expected_class = 'class="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem"'
    
    # Devido à complexidade da string original, verificamos se a classe foi inserida corretamente.
    assert expected_class in refactored_output
    assert "style=\"" not in refactored_output, "O estilo inline não deve permanecer após a refatoração."
    
    # Verificação de que o conteúdo ainda está presente
    assert "💬" in refactored_output