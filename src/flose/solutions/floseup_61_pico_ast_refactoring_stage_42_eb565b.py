import re

def refactor_code(code: str) -> str:
    # Regex to find and replace old-style type hints with new syntax
    code = re.sub(r'Type[ ]*\([a-zA-Z_][a-zA-Z0-9_]*)', r'\1', code)
    return code
