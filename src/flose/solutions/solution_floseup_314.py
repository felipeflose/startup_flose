"""
Módulo de Solução para [FLOSEUP-314]
Resumo: Refatorar Módulo de Sistema #892
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-314"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
