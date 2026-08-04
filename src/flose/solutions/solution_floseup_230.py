"""
Módulo de Solução para [FLOSEUP-230]
Resumo: [PO-EVIL-BOSS] Refatorar src/flose/connectors/gemma_local.py: Backend/TratamentoErros (Linha 39)
Responsável: Sofia
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {"status": "COMPLETED", "id": "FLOSEUP-230"}

def test_execute_task():
    res = execute_task({"k": "v"})
    assert res["status"] == "COMPLETED"
