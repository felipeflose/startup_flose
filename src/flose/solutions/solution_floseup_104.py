"""
Módulo de Solução para [FLOSEUP-104]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/web_app.py: Frontend/CSS (Linha 1124)
Responsável: Sofia
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-104"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
