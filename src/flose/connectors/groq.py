"""
Conector oficial do Groq Cloud (Ultra-Fast LPU Engine — 100% GRATUITO).
Fornece inferência de altíssima velocidade (800 tok/s) com Llama 3.3 70B Versatile.
"""

import urllib.request
import json
import ssl
import os
from typing import Dict, Any, Optional

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

class GroqConnector:
    def __init__(self, api_key: str = None, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.api_key = api_key
        self.model_name = model_name
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def generate_code(self, prompt: str, timeout_sec: int = 30) -> Optional[str]:
        """Gera código via API REST oficial do Groq Cloud (Llama 3.3 70B)."""
        if not self.api_key:
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "FloseUp/1.0"
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "Você é um especialista em desenvolvimento Python e síntese de código AST."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        
        ssl_ctx = ssl.create_default_context()
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=timeout_sec) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[Groq Connector Error] {e}")
            return None
