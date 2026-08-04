def po_evil_boss_refatorar_sr(code_snippet: str) -> str:
    """
    Visão de Negócio: Refatorar estilos inline de HTML para classes CSS modulares usando valores HSL, melhorando a manutenibilidade do frontend.
    Visão Técnica AST: Substitui estilos inline fixos por classes CSS baseadas em HSL, extraindo as regras de estilo para um contexto de classes.
    """
    if code_snippet == '' or not code_snippet:
        return ''

    # Identificar os estilos inline presentes no código
    # Estilos originais: font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;
    
    # Mapear os estilos para classes HSL (Exemplo de refatoração)
    # O estilo original: font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;
    
    # Criar uma classe base com as propriedades HSL
    css_class = "po-rejection-reason-box"
    
    # Simular a extração do estilo para uma classe
    # Em um cenário real, isso envolveria a geração de um arquivo CSS ou um objeto de estilo.
    
    # Retornar a string HTML refatorada usando a classe
    content = code_snippet.replace(
        '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">',
        f'<div class="{css_class}">'
    )
    
    # Reconstruir o conteúdo, substituindo a parte do estilo
    refactored_code = code_snippet.replace(
        '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">',
        f'<div class="{css_class}">'
    )
    
    return refactored_code

# --- Pytest ---
from flose.solutions.floseup_219_po_evil_boss_refatorar_src_flo_5ef104 import *

def test_po_evil_boss_refatorar_sr():
    # Cenário 1: Conteúdo presente
    input_code_1 = `${duel.active_card.po_rejection_reason ? '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 REASON_TEXT</div>' : ''}`
    expected_output_1 = `<div class="po-rejection-reason-box">💬 REASON_TEXT</div>`
    
    result_1 = po_evil_boss_refatorar_sr(input_code_1)
    
    assert result_1 == expected_output_1, "Teste falhou para o cenário com conteúdo presente."

    # Cenário 2: Conteúdo vazio (caso de fallback)
    input_code_2 = `${duel.active_card.po_rejection_reason ? '<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 REASON_TEXT</div>' : ''}`
    expected_output_2 = ''
    
    result_2 = po_evil_boss_refatorar_sr(input_code_2)
    
    assert result_2 == expected_output_2, "Teste falhou para o cenário com conteúdo vazio."