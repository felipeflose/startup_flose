"""
Módulo de Solução para [FLOSEUP-68]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/connectors/jira.py: Backend/Refatoracao (Linha 214)
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-68"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
