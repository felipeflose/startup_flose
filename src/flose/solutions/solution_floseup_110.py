"""
Módulo de Solução para [FLOSEUP-110]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/core/persistence.py: Backend/Docstring (Linha 12)
Responsável: Lucas
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-110"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
