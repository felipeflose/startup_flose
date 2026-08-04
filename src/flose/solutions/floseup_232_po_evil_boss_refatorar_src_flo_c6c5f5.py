"""
Visão de Negócio: Corrigir a função load_env_file no arquivo jira.py para incluir anotações de tipo no retorno.

Visão Técnica AST: Utilizar o módulo ast para varrer e otimizar a árvore sintática do código, adicionando anotações de tipo.
"""

import ast
from typing import Dict, Any

def load_env_file() -> Dict[str, Any]:
    """
    Carrega as variáveis de ambiente de um arquivo .env e retorna como um dicionário.

    Returns:
        Dict[str, Any]: Um dicionário contendo as variáveis de ambiente carregadas.
    """
    env_vars = {}
    with open('.env', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            env_vars[key] = value
    return env_vars