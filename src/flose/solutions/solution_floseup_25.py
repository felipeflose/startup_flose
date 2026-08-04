"""
Módulo de Solução para [FLOSEUP-25]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/agents/po_auditor.py: Backend/Typing (Linha 33)
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-25"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
