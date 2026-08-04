import os
import json
import urllib.request
from typing import Dict, Any, List, Optional

class GemmaLocalConnector:
    """Connector to generate innovation ideas via local Gemma model (Ollama / Local API)."""

    def __init__(self, endpoint: Optional[str] = None, model_name: Optional[str] = None):
        self.endpoint = endpoint or os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.model_name = model_name or os.environ.get("OLLAMA_CODE_MODEL") or os.environ.get("OLLAMA_MODEL") or "gemma4-fast:latest"

    def generate_ideas(self, domain_prompt: str) -> List[Dict[str, Any]]:
        """Generates innovative system features using local Gemma 4."""
        prompt = (
            f"Você é o modelo local {self.model_name} atuando como Gerente de Inovação de Produto do FLOSE AEOS. "
            f"Gere 3 ideias altamente inovadoras e técnicas para: {domain_prompt}. "
            "Retorne um JSON com a lista de ideias, cada uma contendo: title, summary, technical_stack, jira_priority."
        )
        
        # Tentativa de chamada HTTP para Ollama local
        url = f"{self.endpoint}/api/generate"
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
<<<<<<< Updated upstream
            url = f"{self.endpoint}/api/generate"
            payload = {"model": self.model_name, "prompt": prompt, "stream": False}
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
=======
            with urllib.request.urlopen(req, timeout=120) as resp:
>>>>>>> Stashed changes
                data = json.loads(resp.read().decode("utf-8"))
                response_text = data.get("response", "")
                try:
                    return json.loads(response_text)
                except Exception:
                    # Se o LLM não responder um JSON válido, lança erro!
                    raise RuntimeError(f"Ollama respondeu, mas não foi JSON: {response_text}")
        except Exception as e:
            # Sem mock! Lança o erro de verdade pro motor falhar se não tiver LLM!
            raise RuntimeError(f"Ollama local falhou (Host: {self.endpoint}, Modelo: {self.model_name}): {e}")
