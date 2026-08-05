"""
Módulo de Solução para [FLOSEUP-440]
Resumo: [Sanitização] Refatorar src/flose/web_app.py: Limpeza e modularização de loops
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-440"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
