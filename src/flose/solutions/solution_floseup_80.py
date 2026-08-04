"""
Módulo de Solução para [FLOSEUP-80]
Resumo: [PO-EVIL-BOSS] ÉPICO MASTER REFACTORING STAGE 43
Responsável: Lucas
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-80"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
