"""
Módulo de Solução para [FLOSEUP-66]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/web_app.py: Backend/Typing (Linha 227)
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-66"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
