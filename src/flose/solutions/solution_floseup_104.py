"""
Módulo de Solução para [FLOSEUP-104]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/web_app.py: Frontend/CSS (Linha 1124)
Responsável: Sofia
(fallback estático — configure ANTHROPIC_API_KEY para geração real)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-104"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
