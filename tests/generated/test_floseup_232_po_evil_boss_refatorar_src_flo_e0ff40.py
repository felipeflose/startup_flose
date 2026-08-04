from flose.solutions.floseup_232_po_evil_boss_refatorar_src_flo_e0ff40 import load_env_file

def test_load_env_file():
    # Simulando um arquivo .env com dados válidos
    with open('.env', 'w') as file:
        file.write('{"VAR1": "value1", "VAR2": "value2"}')

    env_data = load_env_file()

    assert env_data == {"VAR1": "value1", "VAR2": "value2"}
    assert isinstance(env_data, dict)

    # Simulando um arquivo .env vazio
    with open('.env', 'w') as file:
        file.write('')

    try:
        load_env_file()
    except FileNotFoundError:
        pass

    else:
        assert False, "Deveria ter levantado uma exceção FileNotFoundError"

    # Removendo o arquivo .env criado
    import os
    os.remove('.env')

test_load_env_file()