"""
Visão de Negócio: Testar a função load_env_file para garantir que ela carrega corretamente as variáveis de ambiente.

Visão Técnica AST: Criar testes rigorosos usando Pytest para validar o comportamento da função load_env_file.
"""

import pytest
from flose.solutions.floseup_232_po_evil_boss_refatorar_src_flo_c6c5f5 import load_env_file

def test_load_env_file():
    """
    Testa a função load_env_file para verificar se ela carrega corretamente as variáveis de ambiente.
    """
    # Arrange
    expected_vars = {
        'KEY1': 'value1',
        'KEY2': 'value2'
    }

    # Mock the .env file content
    with open('.env', 'w') as file:
        file.write('KEY1=value1\n')
        file.write('KEY2=value2')

    # Act
    actual_vars = load_env_file()

    # Assert
    assert actual_vars == expected_vars

def test_load_env_file_empty_file():
    """
    Testa a função load_env_file para verificar o comportamento quando o arquivo .env está vazio.
    """
    # Arrange
    expected_vars = {}

    # Mock the .env file content as empty
    with open('.env', 'w') as file:
        pass

    # Act
    actual_vars = load_env_file()

    # Assert
    assert actual_vars == expected_vars

def test_load_env_file_missing_key():
    """
    Testa a função load_env_file para verificar o comportamento quando uma chave não está presente no arquivo .env.
    """
    # Arrange
    expected_vars = {
        'KEY1': 'value1'
    }

    # Mock the .env file content with one key missing
    with open('.env', 'w') as file:
        file.write('KEY1=value1\n')

    # Act
    actual_vars = load_env_file()

    # Assert
    assert actual_vars == expected_vars

def test_load_env_file_with_comments():
    """
    Testa a função load_env_file para verificar o comportamento quando há comentários no arquivo .env.
    """
    # Arrange
    expected_vars = {
        'KEY1': 'value1'
    }

    # Mock the .env file content with comments
    with open('.env', 'w') as file:
        file.write('KEY1=value1\n')
        file.write('# This is a comment\n')

    # Act
    actual_vars = load_env_file()

    # Assert
    assert actual_vars == expected_vars

def test_load_env_file_with_extra_whitespace():
    """
    Testa a função load_env_file para verificar o comportamento quando há espaços extras no arquivo .env.
    """
    # Arrange
    expected_vars = {
        'KEY1': 'value1'
    }

    # Mock the .env file content with extra whitespace
    with open('.env', 'w') as file:
        file.write(' KEY1=value1\n')
        file.write('\nKEY2 = value2 ')

    # Act
    actual_vars = load_env_file()

    # Assert
    assert actual_vars == expected_vars