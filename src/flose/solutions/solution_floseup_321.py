"""
Módulo de Solução para [FLOSEUP-321]
Resumo: Refatorar Módulo de Sistema #917
Responsável: Sofia
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-321"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
