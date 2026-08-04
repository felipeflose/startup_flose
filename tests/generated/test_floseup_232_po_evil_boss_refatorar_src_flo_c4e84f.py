from flose.solutions.floseup_232_po_evil_boss_refatorar_src_flo_c4e84f import load_env_file

def test_load_env_file():
    # Cenário 1: Arquivo .env vazio
    with open('.env', 'w') as file:
        pass
    result = load_env_file()
    assert isinstance(result, dict)
    assert len(result) == 0

    # Cenário 2: Arquivo .env com variáveis de ambiente
    with open('.env', 'w') as file:
        file.write('VAR1=value1\n')
        file.write('VAR2=value2\n')
    result = load_env_file()
    assert isinstance(result, dict)
    assert len(result) == 2
    assert result['VAR1'] == 'value1'
    assert result['VAR2'] == 'value2'

    # Cenário 3: Arquivo .env com variáveis de ambiente vazias
    with open('.env', 'w') as file:
        file.write('VAR1=\n')
        file.write('VAR2=\n')
    result = load_env_file()
    assert isinstance(result, dict)
    assert len(result) == 2
    assert result['VAR1'] == ''
    assert result['VAR2'] == ''

    # Cenário 4: Arquivo .env com espaços em branco no início e fim das chaves e valores
    with open('.env', 'w') as file:
        file.write(' VAR1 = value1 \n')
        file.write(' VAR2 = value2 \n')
    result = load_env_file()
    assert isinstance(result, dict)
    assert len(result) == 2
    assert result['VAR1'] == 'value1'
    assert result['VAR2'] == 'value2'

    # Cenário 5: Arquivo .env com comentários
    with open('.env', 'w') as file:
        file.write('# Comment\n')
        file.write(' VAR1 = value1 \n')
        file.write(' VAR2 = value2 \n')
    result = load_env_file()
    assert isinstance(result, dict)
    assert len(result) == 2
    assert result['VAR1'] == 'value1'
    assert result['VAR2'] == 'value2'