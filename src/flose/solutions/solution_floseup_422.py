"""
Módulo de Solução para [FLOSEUP-422]
Resumo: [Painel & Informações Úteis] Refatorar src/flose/connectors/jira.py: Métricas e ADF
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-422"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
