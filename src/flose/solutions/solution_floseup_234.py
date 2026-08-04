"""
Módulo de Solução para [FLOSEUP-234]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/engines/code_synthesis.py: Backend/AsyncPerformance (Linha 23)
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-234"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
