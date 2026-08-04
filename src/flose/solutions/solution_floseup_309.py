"""
Módulo de Solução para [FLOSEUP-309]
Resumo: Refatorar Módulo de Sistema #541
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-309"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
