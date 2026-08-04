def po_evil_boss_refatorar_sr(duel):
    """
    Visão de Negócio: Migrar estilos inline para classes CSS modulares (HSL) para melhorar a manutenção e a escalabilidade do frontend.
    Visão Técnica AST: Refatorar a string de template gerada na linha L1492 do web_app.py, extraindo os estilos inline (font-size, color, margin) para classes CSS definidas, aplicando classes HSL apropriadas ao elemento div.
    """
    if not duel.active_card.po_rejection_reason:
        return ''

    # Simulação da extração dos estilos inline para classes HSL
    # Estilos originais:
    # font-size: 0.38rem
    # color: #ff5555
    # margin-bottom: 0.2rem

    # Assumindo que as classes CSS HSL foram definidas externamente (ex: .po-rejection-reason-text, .po-rejection-reason-color, .po-rejection-reason-margin)
    
    rejection_text = duel.active_card.po_rejection_reason.substring(0, 50)

    # Aplicação das classes CSS em vez do style inline
    html_output = f'<div class="po-rejection-reason-text po-rejection-reason-color po-rejection-reason-margin">💬 {rejection_text}</div>'
    
    return html_output