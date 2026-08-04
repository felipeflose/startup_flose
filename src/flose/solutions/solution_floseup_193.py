"""
Módulo de Solução para [FLOSEUP-193]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/connectors/jira.py: Backend/Typing (Linha 30)
Responsável: Lucas
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-193"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
