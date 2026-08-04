import ast

def load_env_file() -> dict[str, any]:
    env_vars = {}
    with open('.env', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            env_vars[key] = value
    return env_vars