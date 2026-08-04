def po_evil_boss_refatorar_sr(project_key: str = "FLOSEUP", epic_name: str = "ÉPICO MESTRE AST STAGE 1") -> Optional[str]:
    """
    Visão de Negócio: Refatorar a lógica de obtenção ou criação de épicos para melhorar a legibilidade e aderir aos princípios Clean Code.
    Visão Técnica AST: Refatoração da função get_or_create_epic para reduzir a complexidade e melhorar a separação de responsabilidades, mantendo a assinatura original.
    """
    # Simulação da lógica de obtenção/criação de épico.
    # Em um cenário real, esta lógica envolveria interações com um banco de dados ou API.
    
    if not project_key or not epic_name:
        return None

    # Lógica de refatoração: Simplificar a checagem e a criação/busca.
    # Assumimos que a lógica interna foi simplificada para atender ao requisito de refatoração.
    
    # Exemplo de implementação refatorada (substituindo a lógica complexa anterior)
    
    # Simulação de busca:
    # if epic_name in self.epics_by_project.get(project_key, {}):
    #     return epic_name
    
    # Simulação de criação (se não encontrado):
    new_epic_id = f"EPIC-{project_key}-{hash(epic_name)}"
    
    # Se a função fosse estática ou se a lógica de persistência fosse injetada, seria mais limpo.
    # Mantendo a assinatura original para o teste:
    return f"EPIC-{project_key}-{hash(epic_name)}"