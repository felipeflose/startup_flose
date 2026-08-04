"""
Visão de Negócio: A função 'load_env_file' atualmente carrega um arquivo de ambiente, mas não retorna o tipo dos dados. É necessário adicionar anotações de tipo para melhorar a legibilidade e segurança do código.

Visão Técnica AST: Utilizando o módulo `ast`, vamos varrer o código-fonte em busca da função 'load_env_file' e adicionar anotações de tipo ao retorno da função. Isso envolverá a análise e modificação da árvore abstrata do código Python.
"""

import ast
import json

def load_env_file() -> dict:
    """Carrega um arquivo .env em formato JSON e retorna um dicionário com as variáveis de ambiente.

    Returns:
        dict: Dicionário contendo as variáveis de ambiente carregadas do arquivo .env.

    Raises:
        FileNotFoundError: Se o arquivo .env não for encontrado.
        json.JSONDecodeError: Se houver um erro na decodificação JSON do arquivo.
    """
    try:
        with open('.env', 'r') as file:
            env_data = json.load(file)
        return env_data
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo .env não encontrado.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Erro na decodificação JSON do arquivo .env.")

# Códigos adicionais para carregar variáveis de ambiente podem ser implementados aqui