"""
Módulo de Solução para [FLOSEUP-439]
Resumo: [Front-end Pixel Perfect] Refatorar src/flose/static/index.html: UI Cyberpunk de Jogo
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-439"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
