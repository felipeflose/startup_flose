"""
Conector oficial do Google Antigravity CLI (agy) para orquestração de IA de Alta Razão.
Utiliza a CLI `/Users/felipeflose/.local/bin/agy --print --dangerously-skip-permissions`
para atuar como Motor do Tech Lead Felipe e Motor do PO Vilão.
"""

import subprocess
import asyncio
import os
import json
from typing import Dict, Any, Optional

AGY_BIN = "/Users/felipeflose/.local/bin/agy"

class AgyConnector:
    def __init__(self, bin_path: str = AGY_BIN):
        self.bin_path = bin_path if os.path.exists(bin_path) else "agy"

    async def run_prompt(self, prompt: str, timeout_sec: int = 120) -> str:
        """Executa um prompt de forma não-interativa no Antigravity CLI com permissões de autonomia."""
        cmd = [self.bin_path, "--print", "--dangerously-skip-permissions", prompt]
        try:
            res = await asyncio.to_thread(
                subprocess.run,
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            out = res.stdout.strip()
            return out if out else res.stderr.strip()
        except Exception as e:
            return f"[Agy Error] {e}"

    async def tech_lead_triagem(self, card_title: str, card_desc: str, code_snippet: str) -> Dict[str, Any]:
        """Utiliza o Antigravity CLI como Tech Lead para inspecionar o código e decidir a triagem."""
        prompt = (
            f"Você é o Tech Lead Felipe do time Antigravity.\n"
            f"Analise o card do Jira:\n"
            f"Título: {card_title}\n"
            f"Descrição: {card_desc}\n\n"
            f"Código real do repositório host:\n"
            f"---\n{code_snippet[:1500]}\n---\n\n"
            f"Sua missão: Escolha o Herói ideal entre: LUCAS (Refatoração Python/Rust), SOFIA (Frontend/CSS/UI), BEATRIZ (Ollama/IaC/Infra), FELIPE (Async Core).\n"
            f"Responda EXATAMENTE em formato JSON com duas chaves:\n"
            f"{{\"hero\": \"NOME_DO_HEROI\", \"reason\": \"MOTIVO_TECNICO_DA_ESCALACAO\"}}\n"
        )
        response_text = await self.run_prompt(prompt, timeout_sec=90)
        try:
            # Tenta extrair bloco JSON da resposta
            import re
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception:
            pass
        return {"hero": "LUCAS", "reason": f"Escalado via AGY Engine (Resposta: {response_text[:100]})"}

    async def po_vilao_teach_heroes(self, card_id: str, topic: str, error_log: str) -> str:
        """Utiliza o Antigravity CLI como PO Vilão para analisar uma falha e gerar uma lição de aprendizado."""
        prompt = (
            f"Você é o PO Vilão Sênior atuando como auditor de qualidade Antigravity.\n"
            f"O card [{card_id}] ({topic}) falhou no teste Pytest com o seguinte erro:\n"
            f"---\n{error_log[:1500]}\n---\n\n"
            f"Sua missão: Elabore uma lição técnica clara (1 a 2 parágrafos) ensinando aos heróis como resolver e nunca mais cometer esse erro em desenvolvimentos futuros.\n"
        )
        return await self.run_prompt(prompt, timeout_sec=90)
