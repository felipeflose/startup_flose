def po_evil_boss_refatorar_sr(original_code: str) -> str:
    """
    Visão de Negócio: Melhorar a legibilidade e a manutenibilidade da função de busca/criação de épicos, aplicando princípios do Clean Code.
    Visão Técnica AST: Refatorar a função 'get_or_create_epic' de 50 linhas em um bloco mais coeso, separando a lógica de busca e criação, e garantindo que a função retorne o resultado esperado de forma clara.
    """
    # Simulação da refatoração Clean Code para a função get_or_create_epic
    # Assumindo que a lógica interna envolve busca e criação.
    
    def _find_epic(project_key: str, epic_name: str) -> Optional[str]:
        # Lógica de busca (simulada)
        return None

    def _create_epic(project_key: str, epic_name: str) -> str:
        # Lógica de criação (simulada)
        return f"NEW_EPIC_{project_key}_{epic_name}"

    def get_or_create_epic(self, project_key: str = "FLOSEUP", epic_name: str = "ÉPICO MESTRE AST STAGE 1") -> Optional[str]:
        # Refatoração: Simplificação do fluxo de controle
        epic = _find_epic(project_key, epic_name)
        if epic:
            return epic
        else:
            new_epic = _create_epic(project_key, epic_name)
            # Em um cenário real, aqui se faria a persistência do novo epic.
            return new_epic

    return get_or_create_epic