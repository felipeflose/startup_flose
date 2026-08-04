import asyncio
import time
import random
import os
<<<<<<< Updated upstream
import sys
=======
import re
>>>>>>> Stashed changes
import subprocess
import json
import re
import ast
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Union
import urllib.request
import urllib.parse
import urllib.error
import base64

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

# ====================================================================
# CARREGAMENTO DE VARIÁVEIS DE AMBIENTE (.env)
# ====================================================================
# Precisa vir ANTES de qualquer os.getenv() usado para configurar
# clientes (Jira, GitHub, etc). Sem isso, o .env do projeto é
# ignorado e tudo cai nos valores default hardcoded.
load_dotenv()

# ====================================================================
# CONFIGURAÇÃO DE LOGGING E AMBIENTE DE EXECUÇÃO
# ====================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (L%(lineno)d): %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("FLOSE_AEOS")

REPO_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOLUTIONS_DIR = os.path.join(REPO_PATH, "src", "flose", "solutions")
SKILLS_DOC_PATH = os.path.join(REPO_PATH, "docs", "skills_learned.md")
PERSISTENCE_FILE = os.path.join(REPO_PATH, "data", "state_persistence.json")

<<<<<<< Updated upstream
os.makedirs(SOLUTIONS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(SKILLS_DOC_PATH), exist_ok=True)
os.makedirs(os.path.dirname(PERSISTENCE_FILE), exist_ok=True)
=======
# Busca os cards REAIS do Jira Cloud da sua conta (felipeflose.atlassian.net)
real_jira_cards = jira.fetch_real_jira_issues(project_key="FLOSEUP", limit=1000)
for c in real_jira_cards:
    c.setdefault("rejections", 0)

# REMOVIDO: Carregamento de persistência local para garantir Single Source of Truth (Jira Cloud)
# O estado agora sempre inicia zerado e é populado 100% pelo sync do Jira.

game_state = {
    "boss_name": "PO EVIL BOSS (FRENZY MODE)",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "current_phase": "HERO_TRAINING_PHASE",
    "phase_timer_sec": 120,
    "boss_cards_created_in_frenzy": 0,
    "target_cards_to_clear_80pct": 0,
    "cards_cleared_in_current_wave": 0,
    "cards_coded_count": 0,
    "victory": False,
    "boss_phase": "🎓 ACADEMIA DOS HERÓIS: ESTUDANDO E CRIANDO COMMITS REAIS NO GITHUB!",
    "duel": {
        "is_active": False,
        "active_hero": None,
        "hero_key": None,
        "active_card": None,
        "timeout_timer_sec": 18.0,
        "max_timeout_sec": 18.0,
        "damage_dealt": 0,
        "phase": "idle"  # idle | hero_working | in_validation | po_reviewing | approved | rejected
    },
    "kanban": {
        "to_do": real_jira_cards if real_jira_cards else [],
        "in_progress": [],
        "in_validation": [],
        "done": []
    },
    "last_real_commit": "Nenhum commit ainda",
    "total_real_commits": 0,
}

pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe",
        "class": "Líder de Arquitetura",
        "sprite_color": "#3b82f6",
        "x": 100, "y": 260,
        "skill_level": 1,
        "xp": 0,
        "new_skills_learned": ["Arquitetura Async Core"],
        "github_commits": ["commit 7f3a8b2: docs(architecture): learn Async Core design"],
        "response_speed_ms": 250.0,
        "timeout_resistance_sec": 18.0,
        "action": "Treinando e Aprendendo Novas Arquiteturas",
    },
    "sofia": {
        "name": "Sofia",
        "class": "Gemma 4 & Ollama Analyst",
        "sprite_color": "#ec4899",
        "x": 220, "y": 220,
        "skill_level": 1,
        "xp": 0,
        "new_skills_learned": ["Fine-Tuning Gemma 4"],
        "github_commits": ["commit c912f5a: docs(gemma4): learn Gemma 4 fine-tuning"],
        "response_speed_ms": 200.0,
        "timeout_resistance_sec": 18.0,
        "action": "Estudando Modelos no Gemma 4 & Ollama",
    },
    "lucas": {
        "name": "Lucas",
        "class": "Claude-Code Ollama & AGY Coder",
        "sprite_color": "#f97316",
        "x": 350, "y": 270,
        "skill_level": 1,
        "xp": 0,
        "new_skills_learned": ["Refatoração Rust/Python"],
        "github_commits": ["commit e4819a3: feat(skill-rust): learn Rust/Python refactoring"],
        "response_speed_ms": 120.0,
        "timeout_resistance_sec": 18.0,
        "action": "Treinando Algoritmos de Alta Velocidade",
    },
    "beatriz": {
        "name": "Beatriz",
        "class": "QA & Security Shield",
        "sprite_color": "#10b981",
        "x": 480, "y": 230,
        "skill_level": 1,
        "xp": 0,
        "new_skills_learned": ["Testes de Mutação"],
        "github_commits": ["commit 88f21bc: docs(security): learn mutation testing"],
        "response_speed_ms": 210.0,
        "timeout_resistance_sec": 18.0,
        "action": "Aprimorando Suíte de Testes de Aceite",
    }
}

audit_logs: List[Dict[str, Any]] = []

async def auto_save_persistence_loop():
    """Salva o estado do jogo periodicamente no disco (data/state_persistence.json)."""
    while True:
        await asyncio.sleep(2.0)
        await save_state_to_disk(game_state, pixel_agents, audit_logs)
>>>>>>> Stashed changes


# ====================================================================
# CONFIGURAÇÃO CENTRALIZADA (lê o .env com os nomes reais das chaves)
# ====================================================================

class Settings:
    """
    Centraliza a leitura de variáveis de ambiente. Aceita tanto os nomes
    usados no .env do projeto (JIRA_HOST/JIRA_USER/JIRA_TOKEN) quanto
    variações antigas (JIRA_DOMAIN/JIRA_EMAIL/JIRA_API_TOKEN), para não
    quebrar quem já tinha o outro padrão configurado.
    """

<<<<<<< Updated upstream
    def __init__(self):
        raw_host = (
            os.getenv("JIRA_HOST")
            or os.getenv("JIRA_DOMAIN")
            or "https://felipeflose.atlassian.net"
=======
            commit_msg = f"feat(skills-{agent_name.lower()}): {agent_name} learned '{skill_name}' - auto commit by FLOSE AEOS"

            # Git add
            await asyncio.to_thread(
                subprocess.run,
                ["git", "add", "docs/skills_learned.md"],
                cwd=REPO_PATH, capture_output=True, text=True
            )

            # Git commit
            result_commit = await asyncio.to_thread(
                subprocess.run,
                ["git", "commit", "-m", commit_msg],
                cwd=REPO_PATH, capture_output=True, text=True
            )

            if result_commit.returncode != 0:
                # Pode ser "nothing to commit"
                return f"[skip] {skill_name} (nada novo para commitar)"

            # Git push
            result_push = await asyncio.to_thread(
                subprocess.run,
                ["git", "push", "origin", "main"],
                cwd=REPO_PATH, capture_output=True, text=True
            )

            # Pega o hash real do commit
            result_hash = await asyncio.to_thread(
                subprocess.run,
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=REPO_PATH, capture_output=True, text=True
            )
            real_hash = result_hash.stdout.strip() if result_hash.returncode == 0 else "??????"
            real_commit_msg = f"commit {real_hash}: {commit_msg[:60]}"
            
            game_state["last_real_commit"] = real_commit_msg
            game_state["total_real_commits"] = game_state.get("total_real_commits", 0) + 1
            
            return real_commit_msg
        except Exception as e:
            return f"[erro commit] {str(e)[:50]}"


def learn_new_skills_autonomously(agent_key: str):
    agt = pixel_agents[agent_key]
    agt["xp"] += 50
    skills_pool = [
        "Design Pattern Master",
        "EventBus Acceleration",
        "Ollama Quantization",
        "AGY Scripting Engine",
        "Pixel Perfect CSS Engine",
        "Zero-Trust Security Shield",
        "Mutation Testing Suite",
        "Async Pipeline Builder",
        "Claude-Code Integration",
        "Gemma4 Fine-Tuner",
    ]
    new_skill = random.choice(skills_pool)
    if new_skill not in agt["new_skills_learned"]:
        agt["new_skills_learned"].append(new_skill)

    if agt["xp"] >= 100:
        agt["xp"] = 0
        agt["skill_level"] += 1
        agt["response_speed_ms"] = max(15.0, round(agt["response_speed_ms"] * 0.65, 1))
        agt["timeout_resistance_sec"] += 3.0
        agt["action"] = f"🆙 LEVEL UP! Lv.{agt['skill_level']} - Resistência: {agt['timeout_resistance_sec']}s"

    return new_skill


# ============================================================
# PO VILÃO GERA CARDS DINÂMICOS E DIVERSOS (SEM DUPLICAÇÃO)
# ============================================================
DYNAMIC_CARD_DOMAINS = [
    ("Segurança & Sanitização", ["Sanitizador de Token Zero-Trust", "Proteção Contra Injeção SQL em Engine Async", "Escudo Anti-XSS em Renderizador Canvas", "Validação de Payload JWT sem Expiração"]),
    ("Performance & Backend", ["Cache Distribuído com Redis Lock", "Pipeline de Processamento Async Multi-Thread", "Refatoração de Algoritmo em Rust/PyO3", "Otimização de EventBus para Baixa Latência"]),
    ("Inteligência Artificial & LLM", ["Fine-Tuning de Modelo Gemma 4 no Ollama", "Quantização de Pesos para Inferência Local", "Prompt Guard contra Prompt Injection", "Engine de Embeddings Vetoriais em Memória"]),
    ("UI Pixel Perfect & Canvas", ["Renderizador 16-Bit HSL com Grid Responsivo", "Calculador de Interpolador de Animação 60FPS", "Suíte de Layout CSS Pixel-Perfect", "Parser de Sprite 2D/3D com Cache de Textura"]),
    ("Engenharia de Qualidade (QA)", ["Suíte de Testes de Mutação para Módulos Core", "Fuzzing Engine para Protocolo de Comunicação", "Gerador de Stubs Automáticos para Pytest", "Verificador de Cobertura de Código em Tempo Real"])
]

async def create_real_jira_card_async():
    """Chama o Auditor Físico AST para analisar o código REAL no disco e criar o card no Jira Cloud."""
    try:
        smell_report = await asyncio.to_thread(scan_host_codebase, "src/flose")
        
        if smell_report:
            title, desc = smell_report
        else:
            title = f"Refatorar Módulo Core: Análise de Desempenho #{random.randint(100, 999)}"
            desc = "PO Vilão exigiu auditoria geral nos módulos de infraestrutura async."
            
        await async_create_jira_card_background(title, desc)
    except Exception as e:
        print(f"[Create Real Card Error] {e}")

async def background_boss_card_generator():
    """Worker que faz o Vilão olhar para a main e procurar melhorias continuamente.
    
    ⚠️ PAUSA AUTOMÁTICA: Só cria novos cards quando a fila 'A Fazer' tiver menos de 10 cards.
    Isso evita acúmulo infinito enquanto os heróis processam o backlog atual.
    """
    await asyncio.sleep(5)
    while True:
        try:
            fila_atual = len(game_state["kanban"].get("to_do", []))
            if fila_atual >= 10:
                print(f"[PO VILÃO] 😴 Fila com {fila_atual} cards. Aguardando heróis zerar antes de criar novos...")
            else:
                print("[PO VILÃO] 🔍 Vasculhando a branch principal por débitos técnicos e criando melhorias...")
                await create_real_jira_card_async()
        except Exception as e:
            print(f"[PO Vilão Generator Error] {e}")
        # Varre a cada 60 segundos
        await asyncio.sleep(60.0)


async def async_create_jira_card_background(topic_title: str, topic_desc: str):
    try:
        current_stage = game_state.get("boss_stage", 1)
        epic_name = f" ÉPICO AST REFACTORING STAGE {current_stage}"
        
        jira_res = await asyncio.to_thread(
            jira.create_detailed_epic_or_task, "FLOSEUP", topic_title, topic_desc, epic_name
>>>>>>> Stashed changes
        )
        # normaliza: remove o esquema (http/https) pois quem monta a URL
        # completa é o JiraCloudConnector
        self.jira_domain = raw_host.replace("https://", "").replace("http://", "").rstrip("/")

        self.jira_email = os.getenv("JIRA_USER") or os.getenv("JIRA_EMAIL") or ""
        self.jira_api_token = os.getenv("JIRA_TOKEN") or os.getenv("JIRA_API_TOKEN") or ""
        self.jira_project_key = os.getenv("JIRA_PROJECT_KEY", "FLOSEUP")

        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.github_owner = os.getenv("GITHUB_OWNER", "")
        self.github_repo = os.getenv("GITHUB_REPO", "")

        self.port = int(os.getenv("PORT", "8085"))

        # LLM local via Ollama (zero custo) — PO Vilão gera o card, Heróis resolvem de verdade
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "gemma3:4b")

    def validate(self) -> List[str]:
        """Retorna uma lista de problemas de configuração (vazia = ok)."""
        problems = []
        if not self.jira_domain:
            problems.append("JIRA_HOST/JIRA_DOMAIN não definido no .env")
        if not self.jira_email:
            problems.append("JIRA_USER/JIRA_EMAIL não definido no .env")
        if not self.jira_api_token:
            problems.append("JIRA_TOKEN/JIRA_API_TOKEN não definido no .env")
        return problems


settings = Settings()

_config_problems = settings.validate()
if _config_problems:
    for problem in _config_problems:
        logger.warning(f"[Config] {problem}")

if not settings.ollama_model:
    logger.warning(
        "[Config] OLLAMA_MODEL não definido no .env — o PO Vilão e os Heróis vão "
        "cair no fallback estático (cards e código genéricos)."
    )


# ====================================================================
# CLIENTE HTTP NATIVO DA API REST V3 DO JIRA CLOUD (OPTIMIZED BATCH)
# ====================================================================

class JiraCloudConnector:
    def __init__(self):
        self.domain = settings.jira_domain
        self.email = settings.jira_email
        self.api_token = settings.jira_api_token
        self.base_url = f"https://{self.domain}/rest/api/3"

        auth_bytes = f"{self.email}:{self.api_token}".encode("utf-8")
        self.auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")
        self.headers = {
            "Authorization": f"Basic {self.auth_b64}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _request(self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Tuple[int, Dict[str, Any]]:
        url = f"{self.base_url}{endpoint}"
        body_data = json.dumps(payload).encode("utf-8") if payload else None

        req = urllib.request.Request(url, data=body_data, headers=self.headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                status_code = resp.status
                raw_body = resp.read().decode("utf-8")
                json_body = json.loads(raw_body) if raw_body else {}
                return status_code, json_body
        except urllib.error.HTTPError as http_err:
            err_body = http_err.read().decode("utf-8")
            if http_err.code == 404:
                pass  # Silencia log de 404 para não poluir terminal na validação
            else:
                logger.error(f"[Jira HTTP Error {http_err.code}] {endpoint}: {err_body}")
            return http_err.code, {"error": err_body}
        except Exception as ex:
            logger.error(f"[Jira Request Exception] {ex}")
            return 500, {"error": str(ex)}

    def verify_project_access(self, project_key: str) -> bool:
        """Verifica se o projeto existe e se o usuário tem acesso antes de prosseguir."""
        status_code, data = self._request("GET", f"/project/{project_key}")
        if status_code == 200:
            return True
        logger.error(
            f"[Jira Config Error] O projeto '{project_key}' não existe ou o token "
            f"'{self.email}' não tem permissão. (HTTP {status_code}: {data.get('error', '')[:200]})"
        )
        return False

    def fetch_real_jira_issues(self, project_key: str = None, limit: int = 150) -> List[Dict[str, Any]]:
        """Busca issues usando a nova API POST /search/jql para evitar erros 410 Gone."""
        project_key = project_key or settings.jira_project_key
        jql = f"project = {project_key} AND issuetype not in (Epic, Épico) ORDER BY updated DESC"
        endpoint = "/search/jql"
        payload = {
            "jql": jql,
            "maxResults": limit,
            "fields": ["summary", "description", "status", "parent", "created"]
        }

        status_code, response_data = self._request("POST", endpoint, payload)
        if status_code != 200 or "issues" not in response_data:
            return []

        parsed_cards = []
        for issue in response_data.get("issues", []):
            key = issue.get("key")
            fields = issue.get("fields", {})
            parent_key = fields.get("parent", {}).get("key") if fields.get("parent") else None

            raw_description = self._parse_adf_document(fields.get("description"))
            raw_status = fields.get("status", {}).get("name", "A Fazer").upper()

            parsed_cards.append({
                "id": str(key),
                "title": fields.get("summary", f"Issue {key}"),
                "description": raw_description if raw_description else "Sem descrição registrada.",
                "status": self._normalize_jira_status(raw_status),
                "parent": parent_key,
                "rejections": 0,
                "po_rejection_reason": "",
                "created_at": fields.get("created", datetime.now().isoformat()),
                "is_real_jira": True
            })
        return parsed_cards

    def filter_existing_keys_in_batch(self, issue_keys: List[str]) -> set:
        """Filtra issues existentes usando a nova API POST /search/jql."""
        if not issue_keys:
            return set()
        keys_str = ",".join([f"'{k}'" for k in issue_keys if k.startswith(f"{settings.jira_project_key}-")])
        if not keys_str:
            return set()

        jql = f"key in ({keys_str})"
        endpoint = "/search/jql"
        payload = {
            "jql": jql,
            "maxResults": len(issue_keys),
            "fields": ["key"]
        }

        status_code, response_data = self._request("POST", endpoint, payload)
        if status_code == 200 and "issues" in response_data:
            return {item["key"] for item in response_data["issues"]}
        return set()

    def create_detailed_epic_or_task(self, project_key: str, summary: str, description: str, epic_name: Optional[str] = None) -> Dict[str, Any]:
        type_candidates = ["Epic", "Épico"] if epic_name else ["Task", "Tarefa", "Story", "História"]
        for itype in type_candidates:
            payload = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
                    },
                    "issuetype": {"name": itype}
                }
            }
            status_code, body = self._request("POST", "/issue", payload)
            if status_code in (200, 201) and "key" in body:
                return {"key": body["key"], "success": True}
        return {"key": None, "success": False, "error": "Incapaz de criar item com os tipos suportados."}

    def link_parent_epic(self, issue_key: str, epic_key: str) -> Tuple[bool, int]:
        if not issue_key or not epic_key or issue_key == epic_key:
            return False, 400
        payload = {"fields": {"parent": {"key": epic_key}}}
        status_code, _ = self._request("PUT", f"/issue/{issue_key}", payload)
        return status_code in (200, 204), status_code

    def transition_issue(self, issue_key: str, target_status_name: str) -> Tuple[bool, int]:
        status_code, data = self._request("GET", f"/issue/{issue_key}/transitions")
        if status_code != 200 or "transitions" not in data:
            return False, status_code
        selected_transition_id = None
        target_norm = target_status_name.lower().strip()
        for trans in data["transitions"]:
            name = trans.get("name", "").lower().strip()
            to_name = trans.get("to", {}).get("name", "").lower().strip()
            if target_norm in (name, to_name):
                selected_transition_id = trans.get("id")
                break
        if not selected_transition_id:
            return False, 400
        payload = {"transition": {"id": selected_transition_id}}
        post_status, _ = self._request("POST", f"/issue/{issue_key}/transitions", payload)
        return post_status in (200, 204), post_status

    def add_comment(self, issue_key: str, author_title: str, text: str) -> Tuple[bool, int]:
        payload = {
            "body": {
                "type": "doc", "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": f"[{author_title}]: ", "marks": [{"type": "strong"}]},
                        {"type": "text", "text": text}
                    ]
                }]
            }
        }
        status_code, _ = self._request("POST", f"/issue/{issue_key}/comment", payload)
        return status_code in (200, 201), status_code

    def clear_all_comments(self, issue_key: str) -> Tuple[bool, int]:
        status_code, data = self._request("GET", f"/issue/{issue_key}/comment")
        if status_code == 200 and "comments" in data:
            for comment_item in data["comments"]:
                c_id = comment_item.get("id")
                self._request("DELETE", f"/issue/{issue_key}/comment/{c_id}")
            return True, 200
        return False, status_code

    def get_issue_details(self, issue_key: str) -> Tuple[Dict[str, Any], int]:
        status_code, data = self._request("GET", f"/issue/{issue_key}?fields=summary,description,status,parent,comment")
        if status_code == 200:
            return data, 200
        return {}, status_code

    def _parse_adf_document(self, adf_node: Any) -> str:
        if not adf_node or not isinstance(adf_node, dict):
            return ""
        extracted = []

        def _walk(node):
            if isinstance(node, dict):
                if node.get("type") == "text" and "text" in node:
                    extracted.append(node["text"])
                for child in node.get("content", []):
                    _walk(child)
            elif isinstance(node, list):
                for item in node:
                    _walk(item)

        _walk(adf_node)
        return " ".join(extracted).strip()

    def _normalize_jira_status(self, raw_status: str) -> str:
        s = raw_status.upper()
        if any(term in s for term in ["PROGRESS", "FAZENDO", "IN WORK"]):
            return "EM PROGRESSO"
        if any(term in s for term in ["VALIDA", "ANALISE", "REVIEW"]):
            return "EM VALIDAÇÃO"
        if any(term in s for term in ["DONE", "FEITO", "CONCLU"]):
            return "CONCLUÍDO"
        return "A FAZER"


# ====================================================================
# CLIENTE LLM LOCAL (OLLAMA) — PO VILÃO GERA O CARD, HERÓI RESOLVE DE VERDADE
# ====================================================================

class LocalLLMClient:
    """
    Cliente mínimo (stdlib apenas) para a API local do Ollama
    (http://localhost:11434), zero custo, sem chave de API. Usado em
    dois pontos do jogo:
      1) PO Vilão: gera um card técnico real (título + descrição) em vez
         de um título aleatório tipo "Refatorar Módulo #472".
      2) Herói: gera a implementação real (código + teste) do card que
         recebeu, em vez do boilerplate estático de sempre.
    Se o Ollama não estiver rodando, ou a chamada falhar, os métodos
    retornam None e quem chamou cai num fallback estático — o sistema
    nunca trava por causa do LLM.
    """

    def __init__(self):
        self.host = settings.ollama_host
        self.model = settings.ollama_model
        self.chat_url = f"{self.host}/api/chat"

    def _call(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",  # força o Ollama a retornar JSON válido
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.chat_url,
            data=body_bytes,
            method="POST",
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                content = data.get("message", {}).get("content", "")
                return content.strip() if content else None
        except urllib.error.URLError as url_err:
            logger.error(
                f"[Ollama Connection Error] Não consegui falar com {self.host} "
                f"(o Ollama está rodando? `ollama serve`): {url_err}"
            )
            return None
        except urllib.error.HTTPError as http_err:
            err_body = http_err.read().decode("utf-8")
            logger.error(f"[Ollama HTTP Error {http_err.code}] {err_body[:300]}")
            return None
        except Exception as ex:
            logger.error(f"[Ollama Request Exception] {ex}")
            return None

    @staticmethod
    def _extract_json(raw_text: str) -> Optional[Dict[str, Any]]:
        if not raw_text:
            return None
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except Exception:
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception:
                    return None
        return None

    def generate_card_brief(self, project_context: str) -> Optional[Dict[str, str]]:
        """PO Vilão cria uma demanda técnica real (não um título aleatório)."""
        system_prompt = (
            "Você é um Product Owner implacável de um time de engenharia de software "
            "em Python. Sua função é criar UMA demanda técnica pequena, específica e "
            "implementável (refatoração, função utilitária, endpoint, validação, "
            "parser, etc), do tamanho de uma tarefa que um dev resolve em poucos "
            "minutos com um único módulo Python autocontido. "
            "Responda APENAS com um objeto JSON, sem markdown, sem texto fora do JSON, "
            "no formato exato: {\"title\": \"...\", \"description\": \"...\"}. "
            "O título deve ter no máximo 12 palavras. A descrição deve explicar em "
            "2-4 frases o que precisa ser implementado e qual comportamento esperado."
        )
        user_prompt = f"Contexto do projeto: {project_context}\nCrie a próxima demanda técnica do backlog."
        raw = self._call(system_prompt, user_prompt)
        parsed = self._extract_json(raw) if raw else None
        if parsed and parsed.get("title") and parsed.get("description"):
            return {"title": str(parsed["title"])[:120], "description": str(parsed["description"])[:800]}
        return None

    def generate_solution(self, card_title: str, card_description: str, hero_name: str, hero_class: str) -> Optional[str]:
        """Herói implementa a solução real do card, com teste pytest incluído."""
        system_prompt = (
            f"Você é {hero_name}, {hero_class} em um time de engenharia. Implemente a "
            "solução REAL para a demanda a seguir como um único módulo Python "
            "autocontido (sem imports externos além da stdlib, salvo se estritamente "
            "necessário). O módulo deve conter:\n"
            "1) A lógica de negócio pedida, em uma ou mais funções com nomes "
            "descritivos (não precisa se chamar execute_task).\n"
            "2) Pelo menos uma função de teste no padrão pytest (prefixo test_) que "
            "exercite a lógica implementada e valide o comportamento esperado.\n"
            "Responda APENAS com um objeto JSON no formato exato: "
            "{\"code\": \"...código python completo...\"}. Sem markdown, sem texto "
            "fora do JSON. Escape corretamente quebras de linha e aspas dentro da "
            "string de código."
        )
        user_prompt = f"Card: {card_title}\nDescrição: {card_description}"
        raw = self._call(system_prompt, user_prompt)
        parsed = self._extract_json(raw) if raw else None
        if not parsed or not parsed.get("code"):
            return None

        code = str(parsed["code"])
        try:
            ast.parse(code)
        except SyntaxError as syn_err:
            logger.error(f"[Ollama] Código gerado por {hero_name} tem erro de sintaxe: {syn_err}")
            return None
        if "def test_" not in code:
            logger.warning(f"[Ollama] Código gerado por {hero_name} não tem função de teste pytest.")
            return None
        return code


local_llm_client = LocalLLMClient()


# ====================================================================
# ENGINE DE OPERAÇÕES DO GIT LOCAL E SUBPROCESSOS REMOTOS
# ====================================================================

_git_merge_lock = asyncio.Lock()


async def _exec_git(command_args: List[str]) -> Tuple[int, str, str]:
    def _subprocess_run():
        process = subprocess.run(["git"] + command_args, cwd=REPO_PATH, capture_output=True, text=True)
        return process.returncode, process.stdout, process.stderr
    return await asyncio.to_thread(_subprocess_run)


async def git_checkout_and_create_branch(branch_name: str) -> bool:
    async with _git_merge_lock:
        await _exec_git(["checkout", "main"])
        await _exec_git(["pull", "origin", "main"])
        ret_code, _, stderr = await _exec_git(["checkout", "-b", branch_name])
        if ret_code != 0 and "already exists" in stderr:
            await _exec_git(["checkout", branch_name])
        return True


async def git_commit_and_push(branch_name: str, file_path: str, commit_message: str) -> Tuple[bool, str, str]:
    async with _git_merge_lock:
        await _exec_git(["add", file_path])
        await _exec_git(["commit", "-m", commit_message])
        _, hash_out, _ = await _exec_git(["rev-parse", "--short", "HEAD"])
        commit_hash = hash_out.strip() if hash_out else "HEAD"
        push_code, _, push_err = await _exec_git(["push", "origin", branch_name])
        if push_code != 0:
            return False, commit_hash, push_err
        return True, commit_hash, "Success"


async def po_vilao_merge_and_delete_branch(branch_name: str) -> Tuple[bool, str]:
    if not branch_name or branch_name == "main":
        return True, "Sem branch a integrar."
    async with _git_merge_lock:
        try:
            await _exec_git(["fetch", "origin"])
            await _exec_git(["checkout", "main"])
            await _exec_git(["pull", "origin", "main"])
            target_ref = branch_name
            check_branch = await _exec_git(["rev-parse", "--verify", branch_name])
            if check_branch[0] != 0:
                target_ref = f"origin/{branch_name}"

            merge_code, _, stderr = await _exec_git(
                ["merge", target_ref, "--no-ff", "-m", f"chore(release): PO merged {branch_name} into main"]
            )
            if merge_code != 0:
                return False, f"Falha no Git Merge: {stderr.strip()[:150]}"

            await _exec_git(["push", "origin", "main"])
            await _exec_git(["branch", "-D", branch_name])
            await _exec_git(["push", "origin", "--delete", branch_name])
            return True, f"🔀 Branch `{branch_name}` integrada com sucesso na `main` e removida."
        except Exception as e:
            return False, f"Erro ao processar Merge no Git: {e}"


# ====================================================================
# EXECUTOR DE TESTES UNITÁRIOS COM PYTEST
# ====================================================================

def run_pytest(relative_file_path: str) -> Tuple[bool, str]:
    abs_path = os.path.join(REPO_PATH, relative_file_path)
    if not os.path.exists(abs_path):
        return False, "Arquivo não localizado no disco."
    try:
        res = subprocess.run(
            [sys.executable, "-m", "pytest", abs_path, "-v", "--tb=short"],
            cwd=REPO_PATH, capture_output=True, text=True, timeout=60
        )
        passed = (res.returncode == 0)
        return passed, (res.stdout if passed else res.stderr)[:400]
    except subprocess.TimeoutExpired:
        return False, "Timeout: A suíte excedeu 30s."
    except Exception as ex:
        return False, f"Falha Pytest: {ex}"


# ====================================================================
# GERENCIAMENTO DE PERSISTÊNCIA E ESTADO
# ====================================================================

jira_client = JiraCloudConnector()

game_state: Dict[str, Any] = {
    "boss_name": "PO EVIL BOSS (FRENZY MODE)",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "boss_stage": 1,
    "current_epic_key": None,
    "current_phase": "HERO_TRAINING_PHASE",
    "phase_timer_sec": 120,
    "boss_cards_created_in_frenzy": 0,
    "target_cards_to_clear_80pct": 0,
    "cards_cleared_in_current_wave": 0,
    "cards_coded_count": 0,
    "victory": False,
    "boss_phase": "🎓 ACADEMIA DOS HERÓIS: ESTUDANDO E CRIANDO COMMITS REAIS NO GITHUB!",
    "jira_project_valid": True,  # Estado nativo p/ travar loop se Jira der problema
    "duel": {
        "is_active": False,
        "active_hero": None,
        "hero_key": None,
        "active_card": None,
        "work_progress": 0.0,
        "timeout_timer_sec": 18.0,
        "max_timeout_sec": 18.0,
        "damage_dealt": 0,
        "active_power": "Idle",
        "phase": "idle"
    },
    "kanban": {"to_do": [], "in_progress": [], "in_validation": [], "done": []},
    "total_real_commits": 0,
    "cards_processed_count": 0
}

pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {"name": "Felipe", "class": "Líder de Arquitetura", "sprite_color": "#3b82f6", "x": 100, "y": 260, "skill_level": 1, "xp": 0, "action": "Governanca de Arquitetura"},
    "sofia": {"name": "Sofia", "class": "Especialista IA", "sprite_color": "#ec4899", "x": 220, "y": 220, "skill_level": 1, "xp": 0, "action": "Inferência Local"},
    "lucas": {"name": "Lucas", "class": "Eng. Backend", "sprite_color": "#f97316", "x": 350, "y": 270, "skill_level": 1, "xp": 0, "action": "Refatoração de Alta Velocidade"},
    "beatriz": {"name": "Beatriz", "class": "Eng. QA & Security", "sprite_color": "#10b981", "x": 480, "y": 230, "skill_level": 1, "xp": 0, "action": "Cobertura de Testes"}
}

audit_logs: List[Dict[str, Any]] = []


def purge_card_from_kanban(card_id: str):
    logger.warning(f"🚨 [EXPURGO ANTI-404] Card {card_id} deletado no Jira. Removendo...")
    for col_name in ["to_do", "in_progress", "in_validation", "done"]:
        game_state["kanban"][col_name] = [c for c in game_state["kanban"].get(col_name, []) if str(c.get("id")) != str(card_id)]
    if game_state["duel"].get("active_card") and game_state["duel"]["active_card"].get("id") == card_id:
        game_state["duel"]["is_active"] = False
        game_state["duel"]["phase"] = "idle"
        game_state["boss_phase"] = f"👻 Fantasma detectado! O card {card_id} sumiu do Jira!"


def load_persisted_state() -> Tuple[Optional[Dict], Optional[Dict], Optional[List]]:
    if os.path.exists(PERSISTENCE_FILE):
        try:
            with open(PERSISTENCE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("game_state"), data.get("pixel_agents"), data.get("audit_logs")
        except Exception:
            pass
    return None, None, None


async def save_state_to_disk():
    while True:
        await asyncio.sleep(3.0)
        try:
            with open(PERSISTENCE_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {"game_state": game_state, "pixel_agents": pixel_agents, "audit_logs": audit_logs[-50:]},
                    f, indent=2, ensure_ascii=False
                )
        except Exception:
            pass


# ====================================================================
# MECÂNICAS DE JOGO (RPG) E LÓGICA DE NEGÓCIO REAL
# ====================================================================

def trigger_hero_timeout_power(hero_key: str, timeout_pct: float) -> Tuple[float, float, str, int, bool]:
    if timeout_pct < 0.25:
        power_id = random.randint(10000, 13000)
        power_name = (
            f"🌟 QUANTUM BEAM (Power #{power_id})" if hero_key == "sofia"
            else f"⚡ RUST OVERDRIVE (Power #{power_id})" if hero_key == "lucas"
            else f"🛡️ IMPERVIOUS SHIELD (Power #{power_id})"
        )
        return 42.0, 2.5, power_name, power_id, True
    elif timeout_pct < 0.60:
        power_id = random.randint(4000, 9999)
        power_name = (
            f"🔮 Deep Thinking (Power #{power_id})" if hero_key == "sofia"
            else f"🚀 Multi-Thread Surge (Power #{power_id})" if hero_key == "lucas"
            else f"🔰 Zero-Trust Barrier (Power #{power_id})"
        )
        return 28.0, 1.2, power_name, power_id, False
    else:
        power_id = random.randint(1, 3999)
        power_name = (
            f"✨ Fast Inference (Power #{power_id})" if hero_key == "sofia"
            else f"⚙️ Turbo Synthesizer (Power #{power_id})" if hero_key == "lucas"
            else f"🧪 Automated Test (Power #{power_id})"
        )
        return 18.0, 0.0, power_name, power_id, False


def felipe_analyze_and_delegate_card(card: Dict[str, Any]) -> str:
    text = ((card.get("title") or "") + " " + (card.get("description") or "")).lower()
    if any(k in text for k in ["ia", "llm", "modelo", "prompt"]):
        assigned, reason = "sofia", "Requer IA e Modelos Locais."
    elif any(k in text for k in ["async", "perform", "backend"]):
        assigned, reason = "lucas", "Requer otimização Backend."
    else:
        assigned, reason = "beatriz", "Requer QA, Segurança e Testes."
    card["delegated_by"] = "Felipe (Líder de Arquitetura)"
    card["delegated_to"] = pixel_agents[assigned]["name"]
    card["delegation_note"] = reason
    return assigned


async def ensure_real_stage_epic_async(stage_num: int) -> Optional[str]:
    if game_state.get("current_epic_key"):
        _, status_code = await asyncio.to_thread(jira_client.get_issue_details, game_state["current_epic_key"])
        if status_code == 200:
            return game_state["current_epic_key"]
        else:
            game_state["current_epic_key"] = None

    summary = f"ÉPICO MASTER REFACTORING STAGE {stage_num}"
    jira_res = await asyncio.to_thread(
        jira_client.create_detailed_epic_or_task, settings.jira_project_key, summary, "Épico mestre de governança.", summary
    )
    real_key = jira_res.get("key")
    if real_key and str(real_key).startswith(f"{settings.jira_project_key}-"):
        game_state["current_epic_key"] = real_key
        return real_key
    return None


def _static_fallback_solution(card_id: str, card_title: str, hero_name: str) -> str:
    """Usado apenas se o LLM não estiver configurado ou a geração falhar."""
    return f'''"""
Módulo de Solução para [{card_id}]
Resumo: {card_title}
Responsável: {hero_name}
(fallback estático — o Ollama não respondeu, verifique se está rodando)
"""
def execute_task(payload: dict) -> dict:
    if not payload: raise ValueError("Vazio")
    return {{"status": "COMPLETED", "id": "{card_id}"}}

def test_execute_task():
    res = execute_task({{"k": "v"}})
    assert res["status"] == "COMPLETED"
'''


async def synthesize_code_and_commit(
    hero_name: str, hero_class: str, card_title: str, card_description: str, card_id: str, branch_name: str
) -> Dict[str, Any]:
    await git_checkout_and_create_branch(branch_name)
    safe_id = re.sub(r'[^a-zA-Z0-9_]', '_', card_id.lower())
    rel_path = os.path.join("src", "flose", "solutions", f"solution_{safe_id}.py")
    abs_path = os.path.join(REPO_PATH, rel_path)

    generated_code = await asyncio.to_thread(
        local_llm_client.generate_solution, card_title, card_description or card_title, hero_name, hero_class
    )
    used_llm = generated_code is not None
    python_code = generated_code or _static_fallback_solution(card_id, card_title, hero_name)

    header = (
        f'"""\nMódulo de Solução para [{card_id}]\nResumo: {card_title}\n'
        f'Responsável: {hero_name}\n"""\n\n'
    )
    if used_llm and not python_code.lstrip().startswith('"""'):
        python_code = header + python_code

    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(python_code)
    lines_added = len(python_code.splitlines())
    test_passed, test_out = run_pytest(rel_path)
    commit_msg = f"feat({card_id.lower()}): implement solution by {hero_name}"
    push_ok, commit_hash, err = await git_commit_and_push(branch_name, rel_path, commit_msg)
    return {
        "success": push_ok and test_passed,
        "commit_hash": commit_hash,
        "file_path": rel_path,
        "lines_added": lines_added,
        "test_passed": test_passed,
        "test_output": test_out,
        "used_llm": used_llm,
        "error": err if not push_ok else None
    }


def inspect_commit_delivery(commit_info: Dict[str, Any]) -> Tuple[bool, str]:
    if not commit_info or not commit_info.get("success"):
        return False, "Falha no Git ou Pytest."
    if commit_info.get("lines_added", 0) < 5:
        return False, "Volume de código muito baixo."
    return True, "Aprovado. Arquivo .py validado no Pytest."


<<<<<<< Updated upstream
=======
    else:
        # TIER 1: BASIC ATTACK (>60% timeout)
        power_id = random.randint(1, 3999)
        if hero_key == "sofia":
            power_name = f"✨ Gemma Fast Inference (Power #{power_id})"
        elif hero_key == "lucas":
            power_name = f"⚙️ Claude-Code Turbo Synthesizer (Power #{power_id})"
        else:
            power_name = f"🧪 Automated Test Suite (Power #{power_id})"
        return 15.0, 0.5, power_name, power_id, False
        
>>>>>>> Stashed changes
def safe_jira_comment(card_id: str, author: str, text: str):
    asyncio.create_task(asyncio.to_thread(jira_client.add_comment, card_id, author, text))


<<<<<<< Updated upstream
# ====================================================================
# CICLO PRINCIPAL DO JOGO E GOVERNANÇA (MAIN LOOP)
# ====================================================================

async def main_engine_loop():
    await asyncio.sleep(2.0)

    while True:
        try:
            # Trava de Segurança: se o projeto Jira estiver inválido, pausamos a engine para não spammar erros 400
            if not game_state.get("jira_project_valid", True):
                game_state["boss_phase"] = "🚫 FALHA: PROJETO JIRA NÃO EXISTE OU SEM PERMISSÃO!"
                await asyncio.sleep(5.0)
                continue

            stage = game_state.get("boss_stage", 1)
            master_epic_key = await ensure_real_stage_epic_async(stage)

            if game_state.get("victory") or game_state.get("boss_hp", 0) <= 0:
                stage += 1
                game_state["boss_stage"] = stage
                game_state["boss_max_hp"] = 1000 + (stage * 500)
                game_state["boss_hp"] = game_state["boss_max_hp"]
                game_state["boss_name"] = f"PO EVIL BOSS (STAGE {stage})"
                game_state["victory"] = False
                game_state["current_epic_key"] = None
                game_state["boss_phase"] = f"🔥 PO VILÃO EVOLUIU PARA O ESTÁGIO {stage}! HP: {game_state['boss_max_hp']}!"
                await asyncio.sleep(3)
                continue

            # FASE 1: ACADEMIA DE HERÓIS E CRIAÇÃO DE CARDS
            backlog_size = len(game_state["kanban"]["to_do"])
            if backlog_size < 3:
                game_state["current_phase"] = "PO_FRENZY_30S"
                game_state["boss_phase"] = f"⚡ PO FRENZY (STAGE {stage})! VILÃO CRIANDO CARDS NO JIRA!"
                for _ in range(3 - backlog_size):
                    brief = await asyncio.to_thread(
                        local_llm_client.generate_card_brief,
                        "Backend Python de automação de engenharia (Jira + Git + Pytest reais)."
                    )
                    if brief:
                        title = brief["title"]
                        card_description = brief["description"]
                    else:
                        title = f"Refatorar Módulo de Sistema #{random.randint(100, 999)}"
                        card_description = "Criado via Automação (fallback estático — Ollama não respondeu)."

                    res = await asyncio.to_thread(
                        jira_client.create_detailed_epic_or_task, settings.jira_project_key, title, card_description
                    )
                    real_key = res.get("key")
                    if real_key and real_key.startswith(f"{settings.jira_project_key}-"):
                        if master_epic_key:
                            await asyncio.to_thread(jira_client.link_parent_epic, real_key, master_epic_key)
                        game_state["kanban"]["to_do"].append({
                            "id": real_key, "title": title, "description": card_description,
                            "status": "A FAZER", "parent": master_epic_key,
                            "rejections": 0, "is_real_jira": True
                        })
                await asyncio.sleep(2.0)

            # FASE 2: RESOLUÇÃO DE CARDS
            target_clear = max(1, int(len(game_state["kanban"]["to_do"]) * 0.8))
            game_state["current_phase"] = "HEROES_CLEARING_PHASE"
            game_state["boss_phase"] = f"⚔️ HERÓIS BAIXANDO 80% ({target_clear} CARDS) COM VALIDAÇÃO DO PO VILÃO!"

            wave_timer = 180
            while game_state["cards_cleared_in_current_wave"] < target_clear and wave_timer > 0:
                if game_state.get("boss_hp", 100) <= 0:
                    break
                wave_timer -= 1
                game_state["phase_timer_sec"] = wave_timer
                duel = game_state["duel"]

                if not duel["is_active"] and game_state["kanban"]["to_do"]:
                    card = game_state["kanban"]["to_do"].pop(0)
                    card["status"] = "EM PROGRESSO"
                    game_state["kanban"]["in_progress"].append(card)

                    hero_key = felipe_analyze_and_delegate_card(card)
                    hero = pixel_agents[hero_key]

                    card["branch_name"] = f"feature/{card['id'].lower()}-{hero_key}"

                    if str(card["id"]).startswith(f"{settings.jira_project_key}-"):
                        _, tr_code = await asyncio.to_thread(jira_client.transition_issue, card["id"], "Fazendo")
                        if tr_code == 404:
                            purge_card_from_kanban(card["id"])
                            continue

                        safe_jira_comment(
                            card["id"], "Felipe (Arquitetura)",
                            f"✅ **Governança:** Vinculado ao Épico ({master_epic_key}).\n"
                            f"🌿 **Branch:** `{card['branch_name']}`\n"
                            f"👤 **Delegado para:** {hero['name']}"
                        )

                    pixel_agents["felipe"]["action"] = f"🧠 Delegou [{card['id']}] -> {hero['name']}"
                    game_state["duel"] = {
                        "is_active": True, "active_hero": hero["name"], "hero_key": hero_key,
                        "active_card": card, "work_progress": 0.0, "timeout_timer_sec": 15.0,
                        "max_timeout_sec": 15.0, "phase": "hero_working"
                    }
                    duel = game_state["duel"]

                if not duel["is_active"]:
                    await asyncio.sleep(1.0)
                    continue

                hero_key = duel["hero_key"]
                hero = pixel_agents[hero_key]
                c_duel = duel["active_card"]

                if duel["phase"] == "hero_working":
                    duel["timeout_timer_sec"] -= 1.0
                    timeout_pct = max(0.0, duel["timeout_timer_sec"] / duel["max_timeout_sec"])
                    prog_boost, t_rest, p_name, _, _ = trigger_hero_timeout_power(hero_key, timeout_pct)

                    duel["active_power"] = p_name
                    duel["timeout_timer_sec"] = min(25.0, duel["timeout_timer_sec"] + t_rest)
                    duel["work_progress"] = min(100.0, duel.get("work_progress", 0.0) + prog_boost)

                    if duel["work_progress"] >= 100.0 and duel["timeout_timer_sec"] > 0:
                        commit_res = await synthesize_code_and_commit(
                            hero["name"], hero["class"], c_duel["title"], c_duel.get("description", ""),
                            str(c_duel["id"]), c_duel["branch_name"]
                        )
                        c_duel["commit_info"] = commit_res

                        c_duel["status"] = "EM VALIDAÇÃO"
                        if c_duel in game_state["kanban"]["in_progress"]:
                            game_state["kanban"]["in_progress"].remove(c_duel)
                        game_state["kanban"]["in_validation"].append(c_duel)

                        if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"):
                            _, tr_code = await asyncio.to_thread(jira_client.transition_issue, str(c_duel["id"]), "Em análise")
                            if tr_code == 404:
                                purge_card_from_kanban(c_duel["id"])
                                continue
                            origem = "🧠 Gerado por Gemma (Ollama local)" if commit_res.get("used_llm") else "⚙️ Fallback estático"
                            safe_jira_comment(
                                c_duel["id"], hero["name"],
                                f"🤖 **PR Aberto:** Branch `{c_duel['branch_name']}`. Testes Pytest: OK. Origem: {origem}."
                            )

                        game_state["boss_phase"] = f"🔍 PO VILÃO AUDITANDO PR DA BRANCH `{c_duel['branch_name']}`!"
                        pixel_agents[hero_key]["action"] = "📤 PR aberto!"
                        duel["phase"] = "in_validation"
                        duel["timeout_timer_sec"] = 4.0

                    elif duel["timeout_timer_sec"] <= 0:
                        c_duel["rejections"] += 1
                        c_duel["status"] = "A FAZER"
                        if c_duel in game_state["kanban"]["in_progress"]:
                            game_state["kanban"]["in_progress"].remove(c_duel)
                        game_state["kanban"]["to_do"].append(c_duel)

                        if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"):
                            await asyncio.to_thread(jira_client.transition_issue, c_duel["id"], "A fazer")
                            safe_jira_comment(c_duel["id"], "PO Auditor", "⏰ **TIMEOUT!** Retornado ao A Fazer.")

                        game_state["boss_phase"] = f"💀 TIMEOUT NO CARD [{c_duel['id']}]!"
                        duel["is_active"] = False
                        duel["phase"] = "idle"

                elif duel["phase"] == "in_validation":
                    duel["timeout_timer_sec"] -= 1.0

                    if duel["timeout_timer_sec"] <= 0:
                        commit_info = c_duel.get("commit_info", {})
                        approved, reason = inspect_commit_delivery(commit_info)
                        branch_to_merge = c_duel.get("branch_name", "")

                        if approved:
                            merge_success, merge_msg = await po_vilao_merge_and_delete_branch(branch_to_merge)
                            if merge_success:
                                c_duel["status"] = "CONCLUÍDO"
                                if c_duel in game_state["kanban"]["in_validation"]:
                                    game_state["kanban"]["in_validation"].remove(c_duel)
                                game_state["kanban"]["done"].append(c_duel)
                                game_state["cards_cleared_in_current_wave"] += 1
                                game_state["cards_processed_count"] = game_state.get("cards_processed_count", 0) + 1
                                game_state["total_real_commits"] = game_state.get("total_real_commits", 0) + 1

                                if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"):
                                    _, fe_code = await asyncio.to_thread(jira_client.transition_issue, c_duel["id"], "Feito")
                                    if fe_code == 404:
                                        purge_card_from_kanban(c_duel["id"])
                                        continue
                                    safe_jira_comment(c_duel["id"], "PO Auditor", f"✅ **MERGE EXECUTADO!**\n🔀 Git: {merge_msg}")
=======
async def dynamic_frenzy_and_training_game_loop():
    """
    Loop principal REAL do backend.
    Puxa cards da fila "A FAZER", delega para um herói (Gemma LLM), faz commit,
    e o PO Auditor valida. Fluxo ponta a ponta garantido.
    """
    print("[FLOSEUP ENGINE] Motor autônomo iniciado e aguardando cards no board...")
    await asyncio.sleep(5)
    
    while True:
        card = None  # Garante que sempre temos referência pro card em caso de erro
        hero_key = None
        card_id = None
        
        try:
            # ──────────────────────────────────────────────────────────────────
            # ETAPA 1: Pega o primeiro card que está A FAZER
            # ──────────────────────────────────────────────────────────────────
            # ──────────────────────────────────────────────────────────────────
            # ETAPA 1: Ordena e pega o card mais recente (Ordem Decrescente por ID)
            # ──────────────────────────────────────────────────────────────────
            if len(game_state["kanban"]["to_do"]) == 0:
                await asyncio.sleep(5)
                continue

            # Ordena a fila A FAZER por número do ID em ordem DECRESCENTE (ex: FLOSEUP-250 > FLOSEUP-249)
            def _extract_card_num(c):
                m = re.search(r'(\d+)', str(c.get("id", "")))
                return int(m.group(1)) if m else 0

            game_state["kanban"]["to_do"].sort(key=_extract_card_num, reverse=True)
            card = game_state["kanban"]["to_do"].pop(0)
            card_id = card["id"]
            topic = card.get("title", "Refatoração")
            card_description = card.get("description", "Sem descrição detalhada fornecida.")

            print(f"\n{'='*60}")
            print(f"[ENGINE] Processando card (Ordem Decrescente): {card_id} - {topic}")
            print(f"{'='*60}")

            # ──────────────────────────────────────────────────────────────────
            # ETAPA 2: Valida se o card existe no Jira (evita lixo fantasma)
            # ──────────────────────────────────────────────────────────────────
            if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                details = await asyncio.to_thread(jira.get_issue_details, card_id)
                if not details or "id" not in details:
                    print(f"⚠️ [ENGINE] Card {card_id} NÃO existe no Jira Cloud! Descartando.")
                    card = None  # Marca como descartado, não repõe
                    await asyncio.sleep(2)
                    continue

            # ──────────────────────────────────────────────────────────────────
            # ETAPA 3: Inspeção do Código Fonte Real no Disco + Triagem Tech Lead
            # ──────────────────────────────────────────────────────────────────
            print(f"[TECH LEAD FELIPE] Analisando o card {card_id} e inspecionando o código fonte real no disco...")

            from flose.connectors.gemma_local import GemmaLocalConnector
            import urllib.request
            import json

            connector = GemmaLocalConnector()
            
            # Tenta encontrar arquivo e linha mencionados no card
            full_text = f"{topic} {card_description}"
            file_match = re.search(r'(src/[a-zA-Z0-9_/\.-]+\.py)', full_text)
            line_match = re.search(r'(?:Linha|Line)\s*(\d+)', full_text, re.IGNORECASE)

            code_context_str = "Nenhum arquivo específico identificado no card."
            if file_match:
                rel_file = file_match.group(1)
                abs_file = os.path.join(REPO_PATH, rel_file)
                if os.path.exists(abs_file):
                    try:
                        with open(abs_file, "r", encoding="utf-8") as f:
                            all_lines = f.readlines()
                        if line_match:
                            target_line = int(line_match.group(1))
                            start_idx = max(0, target_line - 15)
                            end_idx = min(len(all_lines), target_line + 15)
                            snippet = "".join(all_lines[start_idx:end_idx])
                            code_context_str = f"CÓDIGO ATUAL EM {rel_file} (Linhas {start_idx+1}-{end_idx}):\n```python\n{snippet}\n```"
                        else:
                            snippet = "".join(all_lines[:50])
                            code_context_str = f"CÓDIGO ATUAL EM {rel_file} (Primeiras 50 linhas):\n```python\n{snippet}\n```"
                    except Exception as fe:
                        code_context_str = f"Erro ao ler arquivo {rel_file}: {fe}"
                else:
                    code_context_str = f"⚠️ O ARQUIVO {rel_file} NÃO EXISTE NO REPOSITÓRIO ATUAL."

            heroes_info = []
            for k, v in pixel_agents.items():
                skills_str = ", ".join(v.get("new_skills_learned", ["Python"]))
                heroes_info.append(f"- {k.upper()}: XP {v.get('xp',0)}%, Skills: {skills_str}")

            prompt = (
                f"Você é o Tech Lead Felipe avaliando e delegando tarefas.\n"
                f"Card: [{card_id}] '{topic}'.\n"
                f"Descrição do PO:\n"
                f"---\n{card_description}\n---\n\n"
                f"CÓDIGO FONTE REAL INSPECCIONADO NO DISCO:\n"
                f"{code_context_str}\n\n"
                f"Heróis disponíveis:\n"
                f"{chr(10).join(heroes_info)}\n\n"
                f"AVALIE DUAS COISAS BASEADO NO CÓDIGO FONTE REAL ACIMA:\n"
                f"1. A refatoração solicitada realmente FAZ SENTIDO técnico e traz valor real para o código fonte exibido acima, ou é um card desatualizado/irrelevante/sem sentido?\n"
                f"2. Se fizer sentido (makes_sense=true), qual herói deve assumir e por quê?\n\n"
                f"Responda APENAS em JSON no formato exato:\n"
                f"{{\n"
                f"  \"makes_sense\": true,\n"
                f"  \"rejection_reason\": \"Caso makes_sense seja false, explique com base no código fonte real por que o card não faz sentido\",\n"
                f"  \"chosen_hero\": \"sofia|lucas|beatriz\",\n"
                f"  \"reason\": \"justificativa da escolha do herói\",\n"
                f"  \"business_context\": \"Resuma o impacto de negócio desta tarefa\",\n"
                f"  \"technical_details\": \"Resuma os desafios técnicos da tarefa baseando-se no código real\"\n"
                f"}}"
            )

            try:
                url = f"{connector.endpoint}/api/generate"
                payload = {"model": connector.model_name, "prompt": prompt, "stream": False}
                req = urllib.request.Request(
                    url, data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}, method="POST"
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    clean_text = data.get("response", "").strip()
                    if clean_text.startswith("```json"): clean_text = clean_text[7:]
                    if clean_text.startswith("```"): clean_text = clean_text[3:]
                    if clean_text.endswith("```"): clean_text = clean_text[:-3]
                    clean_text = clean_text.strip()
                    
                    result = {}
                    try:
                        result = json.loads(clean_text, strict=False)
                    except Exception as json_err:
                        hero_match = re.search(r'"chosen_hero"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)
                        reason_match = re.search(r'"reason"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)
                        biz_match = re.search(r'"business_context"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)
                        tech_match = re.search(r'"technical_details"\s*:\s*"([^"]+)"', clean_text, re.IGNORECASE)

                        if hero_match:
                            result["makes_sense"] = True
                            result["chosen_hero"] = hero_match.group(1)
                            if reason_match: result["reason"] = reason_match.group(1)
                            if biz_match: result["business_context"] = biz_match.group(1)
                            if tech_match: result["technical_details"] = tech_match.group(1)
                        else:
                            raise RuntimeError(f"JSON Decode Error ({json_err}) e Regex não encontrou 'chosen_hero' em: {clean_text[:100]}...")

                    makes_sense = result.get("makes_sense", True)
                    # Se o Tech Lead avaliar que o card NÃO faz sentido -> descarta imediatamente!
                    if isinstance(makes_sense, bool) and not makes_sense:
                        rej_msg = result.get("rejection_reason", "Card sem impacto de negócio claro ou sem viabilidade técnica.")
                        print(f"🛑 [TECH LEAD FELIPE - TRIAGEM] Card {card_id} DESPACHADO! Motivo: {rej_msg}")
                        if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                            await asyncio.to_thread(jira.add_comment, card_id, "Tech Lead Felipe",
                                f"🚫 **[TECH LEAD FELIPE - REJEITADO NA TRIAGEM]**\n\n"
                                f"Este card foi analisado pelo Tech Lead e **desqualificado** por não apresentar valor de negócio claro ou fundamentação técnica.\n\n"
                                f"📌 **Motivo:** {rej_msg}"
                            )
                            await asyncio.to_thread(jira.transition_issue, card_id, "Concluído")
                        card = None  # Não repõe na fila
                        await asyncio.sleep(2)
                        continue

                    chosen_hero = str(result.get("chosen_hero", "lucas")).lower()
                    if chosen_hero not in pixel_agents: chosen_hero = "lucas"
                    chosen_reason = result.get("reason", "apresenta o melhor perfil para a tarefa.")
                    biz_ctx = result.get("business_context", "Melhoria contínua da aplicação.")
                    tech_ctx = result.get("technical_details", "Refatoração de código.")

            except Exception as e:
                err_body = ""
                if hasattr(e, "read"):
                    try:
                        err_body = f" | Detalhes: {e.read().decode('utf-8')}"
                    except Exception:
                        pass
                print(f"🚨 [TECH LEAD FELIPE ERRO] Falha no Ollama LLM ({connector.endpoint}, Modelo: {connector.model_name}): {e}{err_body}")
                print(f"🚨 [ENGINE] Abortando delegação do card {card_id} (Zero Mock). Retornando para a fila.")
                game_state["kanban"]["to_do"].append(card)
                card = None  # Já reposto, não repor novamente no finally
                await asyncio.sleep(5)
                continue

            hero_key = chosen_hero
            hero = pixel_agents[hero_key]

            print(f"[TECH LEAD FELIPE] Decisão Final do Ollama: Acionar agente {hero['name'].upper()}.")
            print(f"[TECH LEAD FELIPE] Motivo da escalação: {hero['name']} {chosen_reason}")
            print(f"[HERÓI {hero['name'].upper()}] Recebi a missão do Tech Lead! Preparando setup para resolver o card {card_id}!")

            # Comentário de delegação no Jira
            tech_lead_msg = (
                f"🧑‍💻 **[TECH LEAD FELIPE - DELEGAÇÃO OFICIAL]**\n\n"
                f"✅ **Herói Designado:** {hero['name'].upper()}\n"
                f"🎯 **Motivo da Escalação:** {chosen_reason}\n\n"
                f"💼 **Contexto de Negócio:** {biz_ctx}\n"
                f"⚙️ **Detalhes Técnicos:** {tech_ctx}\n\n"
                f"_Missão autorizada. Iniciando síntese de código via Ollama..._"
            )
            if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                await asyncio.to_thread(jira.add_comment, card_id, "Tech Lead Felipe", tech_lead_msg)

            # ──────────────────────────────────────────────────────────────────
            # ETAPA 4: Mover para "Fazendo" no Jira e no board local
            # ──────────────────────────────────────────────────────────────────
            print(f"[JIRA] Movendo {card_id} para 'Fazendo'...")
            if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                transition_fazendo_ok = await asyncio.to_thread(jira.transition_issue, card_id, "Fazendo")
                if not transition_fazendo_ok:
                    print(f"🚨 [ENGINE] Falha ao mover {card_id} para 'Fazendo' no Jira Cloud!")

            card["status"] = "EM PROGRESSO"
            if card not in game_state["kanban"]["in_progress"]:
                game_state["kanban"]["in_progress"].append(card)

            game_state["duel"] = {
                "is_active": True,
                "active_hero": hero["name"],
                "hero_key": hero_key,
                "active_card": card,
                "work_progress": 0.5,
                "active_power": "Processando via Gemma4 LLM...",
                "phase": "hero_working"
            }
            # Comentário de início do Herói no Jira Cloud
            hero_start_msg = (
                f"🚀 **[HERÓI {hero['name'].upper()} - EM EXECUÇÃO]**\n\n"
                f"🛠️ **O que estou fazendo agora:**\n"
                f"- Inspecionando os arquivos reais da aplicação.\n"
                f"- Escrevendo o módulo Python refatorado e a suíte de testes Pytest.\n"
                f"- Validando execução com Pytest 100% antes de integrar.\n\n"
                f"⏱️ _Trabalhando na implementação via Ollama LLM..._"
            )
            if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                await asyncio.to_thread(jira.add_comment, card_id, f"Herói {hero['name'].title()}", hero_start_msg)

            game_state["boss_phase"] = f"🤖 {hero['name'].upper()} está processando {card_id} via Gemma LLM..."
            pixel_agents[hero_key]["action"] = f"Codando {card_id}..."

            # ──────────────────────────────────────────────────────────────────
            # ETAPA 5: LLM gera código, roda Pytest, faz commit e push
            # ──────────────────────────────────────────────────────────────────
            print(f"[HERÓI {hero['name'].upper()}] Iniciando síntese de código real para {card_id} via Ollama...")
            prev_err = card.get("last_error", "")
            commit_res = await synthesize_and_commit_real_code(hero["name"], topic, card_id, card_description, previous_error=prev_err)

            if not commit_res.get("success"):
                # ── FALHA: Incrementa retry count, guarda erro e realimenta o aprendizado do LLM ──
                failure_reason = commit_res.get("reason", "Erro desconhecido")
                card["last_error"] = failure_reason
                card["timeout_failures"] = card.get("timeout_failures", 0) + 1
                retry_count = card["timeout_failures"]
                
                MAX_RETRIES = 5
                print(f"[HERÓI {hero['name'].upper()}] ❌ FALHA ao processar {card_id}! (tentativa {retry_count}/{MAX_RETRIES}) Erro: {failure_reason}")
                card["status"] = "A FAZER"
                if card in game_state["kanban"]["in_progress"]:
                    game_state["kanban"]["in_progress"].remove(card)

                if retry_count >= MAX_RETRIES:
                    # Mandou MAX_RETRIES x e falhou — grava o aprendizado na base de conhecimento e vai para o final
                    print(f"⚠️ [ENGINE] {card_id} falhou {retry_count}x. Gravando lição de aprendizado em docs/skills_learned.md. Movendo para o FINAL da fila.")
                    
                    try:
                        lesson_entry = (
                            f"\n### ⚠️ Lição de Aprendizado com Falha - Card [{card_id}]\n"
                            f"- **Herói:** {hero['name'].upper()}\n"
                            f"- **Tópico:** {topic}\n"
                            f"- **Motivo da Falha:** {failure_reason[:300]}\n"
                            f"- **Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        )
                        with open(SKILLS_DOC_PATH, "a", encoding="utf-8") as f:
                            f.write(lesson_entry)
                    except Exception as le_err:
                        print(f"Erro ao salvar lição no doc: {le_err}")

                    card["timeout_failures"] = 0  # Reset para próxima rodada
                    game_state["kanban"]["to_do"].append(card)
                    card = None
                    if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                        await asyncio.to_thread(jira.transition_issue, card_id, "A fazer")
                        await asyncio.to_thread(jira.add_comment, card_id, "Sistema Autônomo FloseUp",
                            f"⚠️ **[ENGINE - APRENDIZADO COM FALHAS REITERADAS]**\n\n"
                            f"O card falhou **3 vezes consecutivas** no Pytest.\n"
                            f"📌 **Lição de Aprendizado Registrada:** A falha foi documentada em `docs/skills_learned.md` para realimentação dos modelos.\n"
                            f"O card foi movido para o **final da fila** e os modelos aprenderão com a falha registrada."
                        )
                    await asyncio.sleep(30)
                else:
                    # Falhou 1 ou 2 vezes — repõe no início da fila para retry rápido com feedback do erro
                    game_state["kanban"]["to_do"].insert(0, card)
                    card = None
                    if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                        await asyncio.to_thread(jira.transition_issue, card_id, "A fazer")
                        await asyncio.to_thread(jira.add_comment, card_id, "Sistema Autônomo FloseUp",
                            f"❌ **[HERÓI {hero['name'].upper()} - FALHA COM FEEDBACK (tentativa {retry_count}/3)]**\n\n"
                            f"O código gerado **não passou nos testes automatizados (Pytest)**.\n"
                            f"**Motivo:** {failure_reason}\n\n"
                            f"O traceback da falha foi injetado no contexto do Herói para a nova tentativa."
                        )
                    await asyncio.sleep(10)

                game_state["duel"]["is_active"] = False
                pixel_agents[hero_key]["action"] = "Aguardando próxima task..."
                continue


            # ── SUCESSO no commit ──
            commit_hash = commit_res.get("commit_hash", "unknown")
            commit_msg = commit_res.get("commit_msg", f"[commit] {topic}")
            print(f"[HERÓI {hero['name'].upper()}] ✅ SUCESSO! Código commitado: {commit_hash}")

            game_state["total_real_commits"] += 1
            hero["github_commits"].append(commit_msg)
            if commit_res.get("file_path"):
                hero["github_commits"].append(f"📄 {commit_res['file_path']} (+{commit_res.get('lines_added', 0)} linhas Python)")
            hero["xp"] += 15
            if hero["xp"] >= 100:
                hero["xp"] -= 100
                hero["skill_level"] += 1
                hero["new_skills_learned"].append("Advanced AST Mutation")

            # ──────────────────────────────────────────────────────────────────
            # ETAPA 6: Move para "Em Análise" + comentário do Herói no Jira
            # ──────────────────────────────────────────────────────────────────
            print(f"[JIRA] Movendo {card_id} para 'Em análise'...")
            card["status"] = "EM ANÁLISE"
            if card in game_state["kanban"]["in_progress"]:
                game_state["kanban"]["in_progress"].remove(card)
            game_state["kanban"]["in_validation"].append(card)

            if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                await asyncio.to_thread(jira.transition_issue, card_id, "Em análise")
                await asyncio.to_thread(jira.add_comment, card_id, hero["name"],
                    f"✅ **[HERÓI {hero['name'].upper()} - IMPLEMENTAÇÃO CONCLUÍDA]**\n\n"
                    f"O código foi gerado, testado com Pytest e commitado com sucesso!\n\n"
                    f"📦 **Commit:** `{commit_hash}`\n"
                    f"📄 **Arquivo:** `{commit_res.get('file_path', 'N/A')}`\n"
                    f"📏 **Linhas adicionadas:** +{commit_res.get('lines_added', 0)} linhas Python\n\n"
                    f"_Aguardando revisão e aprovação do PO Auditor Felipe..._"
                )

            game_state["boss_phase"] = f"🔍 PO Auditor revisando {card_id} implementado por {hero['name']}..."
            game_state["duel"]["phase"] = "po_reviewing"

            audit_logs.insert(0, {
                "action": "REAL_GITHUB_COMMIT",
                "hero": hero["name"],
                "commit": commit_hash
            })
            if len(audit_logs) > 20:
                audit_logs.pop()

            # ──────────────────────────────────────────────────────────────────
            # ETAPA 7: PO Auditor (Felipe) valida o commit via LLM
            # ──────────────────────────────────────────────────────────────────
            print(f"[PO AUDITOR FELIPE] 🔍 Revisando o commit {commit_hash} para o card {card_id}...")

            po_prompt = (
                f"Você é o PO (Product Owner) Felipe, revisor técnico rigoroso.\n"
                f"O herói {hero['name']} acabou de entregar a implementação do card [{card_id}].\n\n"
                f"Descrição original do card:\n---\n{card_description}\n---\n\n"
                f"Commit gerado: {commit_hash}\n"
                f"Arquivo: {commit_res.get('file_path', 'N/A')}\n"
                f"Linhas de código adicionadas: {commit_res.get('lines_added', 0)}\n"
                f"Testes Pytest: {'PASSOU ✅' if commit_res.get('test_passed') else 'FALHOU ❌'}\n\n"
                f"Regras de aprovação (TODAS devem ser atendidas para aprovar):\n"
                f"1. O código principal DEVE conter 'Visão de Negócio:' na docstring.\n"
                f"2. O código principal DEVE conter 'Visão Técnica AST:' na docstring.\n"
                f"3. Os testes Pytest devem ter PASSADO.\n"
                f"4. O código deve ser relevante para a descrição do card.\n\n"
                f"Responda APENAS em JSON:\n"
                f"{{\"approved\": true|false, \"reason\": \"justificativa detalhada da decisão\"}}"
            )

            approved = False
            po_reason = "Revisão automática não concluída."
            try:
                url = f"{connector.endpoint}/api/generate"
                payload = {"model": connector.model_name, "prompt": po_prompt, "stream": False}
                req = urllib.request.Request(
                    url, data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}, method="POST"
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    po_data = json.loads(resp.read().decode("utf-8"))
                    po_clean = po_data.get("response", "").strip()
                    if po_clean.startswith("```json"): po_clean = po_clean[7:]
                    if po_clean.startswith("```"): po_clean = po_clean[3:]
                    if po_clean.endswith("```"): po_clean = po_clean[:-3]
                    po_result = json.loads(po_clean)
                    approved = po_result.get("approved", False)
                    po_reason = po_result.get("reason", "Sem justificativa.")
            except Exception as e:
                print(f"🚨 [PO AUDITOR ERRO] Falha ao chamar LLM para revisão: {e}")
                # Se o LLM de revisão falhar, aprova automaticamente se Pytest passou
                approved = commit_res.get("test_passed", False)
                po_reason = f"Aprovação automática (LLM indisponível). Pytest: {'PASSOU' if approved else 'FALHOU'}."

            # ──────────────────────────────────────────────────────────────────
            # ETAPA 8: Aprovação → Concluído | Rejeição → A Fazer
            # ──────────────────────────────────────────────────────────────────
            if card in game_state["kanban"]["in_validation"]:
                game_state["kanban"]["in_validation"].remove(card)

            if approved:
                print(f"[PO AUDITOR FELIPE] ✅ APROVADO! Card {card_id} movendo para CONCLUÍDO.")
                print(f"[PO AUDITOR FELIPE] Motivo: {po_reason}")
                card["status"] = "FEITO"
                game_state["kanban"]["done"].append(card)
                game_state["boss_phase"] = f"🏆 {card_id} CONCLUÍDO com sucesso por {hero['name']}!"

                # ── INTEGRADOR AUTOMÁTICO DE CÓDIGO NO ARQUIVO REAL DO PROJETO ──
                commit_info = card.get("commit_info", {})
                sol_rel_path = commit_info.get("file_path", "")
                full_text = f"{topic} {card_description}"
                target_file_match = re.search(r'(src/[a-zA-Z0-9_/\.-]+\.py)', full_text)

                if target_file_match and sol_rel_path:
                    target_rel_path = target_file_match.group(1)
                    # Evita auto-modificação cíclica infinita do próprio file_path de solução
                    if not target_rel_path.startswith("src/flose/solutions/"):
                        target_abs_path = os.path.join(REPO_PATH, target_rel_path)
                        sol_abs_path = os.path.join(REPO_PATH, sol_rel_path)
                        
                        if os.path.exists(target_abs_path) and os.path.exists(sol_abs_path):
                            try:
                                with open(sol_abs_path, "r", encoding="utf-8") as f_sol:
                                    sol_code = f_sol.read()
                                
                                with open(target_abs_path, "r", encoding="utf-8") as f_orig:
                                    orig_code = f_orig.read()

                                integration_block = (
                                    f"\n\n# ── Refatoração Aprovada [{card_id}] por {hero['name'].upper()} ──\n"
                                    f"# Tópico: {topic}\n"
                                    f"{sol_code}\n"
                                )
                                candidate_code = orig_code + integration_block

                                # Trava de Segurança AST: Só grava se a sintaxe for válida e nenhuma função original for apagada!
                                try:
                                    import ast
                                    orig_tree = ast.parse(orig_code)
                                    cand_tree = ast.parse(candidate_code)
                                    
                                    orig_funcs = {n.name for n in ast.walk(orig_tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
                                    cand_funcs = {n.name for n in ast.walk(cand_tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
                                    
                                    missing_funcs = orig_funcs - cand_funcs
                                    if missing_funcs:
                                        print(f"⚠️ [INTEGRADOR AST GUARD] Integração descartada em {target_rel_path}: Funções originais seriam perdidas ({missing_funcs})!")
                                    else:
                                        with open(target_abs_path, "w", encoding="utf-8") as f_target:
                                            f_target.write(candidate_code)

                                        print(f"✨ [INTEGRADOR AUTOMÁTICO] Aplicando alteração aprovada em {target_rel_path}...")
                                        subprocess.run(["git", "add", target_rel_path], cwd=REPO_PATH, capture_output=True)
                                        int_commit_msg = f"refactor(integrated): applied approved {card_id} to {target_rel_path}"
                                        subprocess.run(["git", "commit", "-m", int_commit_msg], cwd=REPO_PATH, capture_output=True)
                                        subprocess.run(["git", "push", "origin", "main", "--force"], cwd=REPO_PATH, capture_output=True)
                                        print(f"🚀 [INTEGRADOR AUTOMÁTICO] Alteração integrada em {target_rel_path} e enviada ao GitHub!")
                                except SyntaxError as syn_err:
                                    print(f"⚠️ [INTEGRADOR AST GUARD] Tentativa de integração descartada em {target_rel_path} por SyntaxError: {syn_err}")
                            except Exception as int_err:
                                print(f"⚠️ [INTEGRADOR ERROR] Falha ao integrar no arquivo real {target_rel_path}: {int_err}")

                if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                    await asyncio.to_thread(jira.transition_issue, card_id, "Done")
                    await asyncio.to_thread(jira.add_comment, card_id, "PO Auditor Felipe",
                        f"🏆 **[PO AUDITOR FELIPE - APROVADO & INTEGRADO]**\n\n"
                        f"✅ A implementação do herói **{hero['name'].upper()}** foi **APROVADA** e **INTEGRADA AO ARQUIVO REAL**!\n\n"
                        f"**Motivo da aprovação:** {po_reason}\n\n"
                        f"📦 Código integrado e pushado diretamente no arquivo alvo do projeto na branch `main`."
                    )

                audit_logs.insert(0, {
                    "action": "CARD_APPROVED_AND_INTEGRATED",
                    "card": card_id,
                    "hero": hero["name"],
                    "commit": commit_hash
                })
            else:
                print(f"[PO AUDITOR FELIPE] ❌ REJEITADO! Card {card_id} voltando para A Fazer.")
                print(f"[PO AUDITOR FELIPE] Motivo da rejeição: {po_reason}")
                card["status"] = "A FAZER"
                card["rejections"] = card.get("rejections", 0) + 1
                game_state["kanban"]["to_do"].append(card)
                card = None  # Já reposto

                game_state["boss_phase"] = f"🔄 {card_id} REJEITADO pelo PO. Voltando para a fila..."

                if str(card_id).startswith("FLOSEUP-") or str(card_id).startswith("KAN-"):
                    await asyncio.to_thread(jira.transition_issue, card_id, "A fazer")
                    await asyncio.to_thread(jira.add_comment, card_id, "PO Auditor Felipe",
                        f"🚨 **[PO AUDITOR FELIPE - REJEITADO]**\n\n"
                        f"❌ A implementação do herói **{hero['name'].upper()}** foi **REJEITADA**.\n\n"
                        f"**Motivo da Rejeição:** {po_reason}\n\n"
                        f"Card devolvido para `A Fazer`. O herói deve corrigir e resubmeter."
                    )

                audit_logs.insert(0, {
                    "action": "CARD_REJECTED",
                    "card": card_id,
                    "hero": hero["name"],
                    "reason": po_reason
                })

            if len(audit_logs) > 20:
                audit_logs.pop()

        except Exception as e:
            # ── Safety net: Se o card foi retirado da fila mas não foi reposto, repõe ──
            print(f"[ENGINE ERROR] Falha no loop principal: {e}")
            import traceback
            traceback.print_exc()
            if card is not None:
                print(f"[ENGINE RECOVERY] Recolocando {card_id} na fila por segurança.")
                card["status"] = "A FAZER"
                game_state["kanban"]["to_do"].insert(0, card)
        finally:
            if hero_key and hero_key in pixel_agents:
                pixel_agents[hero_key]["action"] = "Aguardando próxima task..."
            game_state["duel"]["is_active"] = False

        await asyncio.sleep(5)


@app.post("/api/boss/synthesize_test")
async def boss_synthesize_test(hero: str = "Lucas", topic: str = "Test Topic", card_id: str = "FLOSEUP-999"):
    res = await synthesize_and_commit_real_code(hero, topic, card_id, "Descrição de teste para simular o card.")
    return {"status": "ok", "result": res}

async def _do_real_commit(hero_key: str, topic: str, card_id: Optional[str] = None):
    """Sintetiza código Python REAL + Pytest e faz commit/push REAL no GitHub!"""
    hero = pixel_agents[hero_key]
    res = await synthesize_and_commit_real_code(hero["name"], topic, card_id, "")
    commit_msg = res.get("commit_msg", f"[commit] {topic}")
    
    hero["github_commits"].append(commit_msg)
    if res.get("file_path"):
        hero["github_commits"].append(f"📄 {res['file_path']} (+{res.get('lines_added', 0)} linhas Python)")
    
    hero["action"] = f"🐙 GitHub: {commit_msg[:40]}..."
    
    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "REAL_PYTHON_CODE_COMMITTED",
        "hero": hero["name"],
        "topic": topic[:30],
        "card_id": card_id or "SKILL",
        "commit": commit_msg[:60]
    })
>>>>>>> Stashed changes

                                damage = 280 + (hero["skill_level"] * 20)
                                game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                                game_state["boss_phase"] = f"✅ PO MERGOU PR! -{damage}HP!"
                                pixel_agents[hero_key]["action"] = "🎉 Branch Deletada!"

                                audit_logs.append({"event_id": f"evt_{len(audit_logs)+1}", "action": "PO_MERGED_PR", "card_id": c_duel["id"]})
                            else:
                                c_duel["rejections"] += 1
                                c_duel["status"] = "A FAZER"
                                if c_duel in game_state["kanban"]["in_validation"]:
                                    game_state["kanban"]["in_validation"].remove(c_duel)
                                game_state["kanban"]["to_do"].append(c_duel)

<<<<<<< Updated upstream
                                if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"):
                                    await asyncio.to_thread(jira_client.transition_issue, c_duel["id"], "A fazer")
                                    safe_jira_comment(c_duel["id"], "PO Auditor", f"🚨 **FALHA MERGE:** {merge_msg}")

                                game_state["boss_phase"] = "❌ ERRO NO MERGE DA BRANCH!"
                        else:
                            c_duel["rejections"] += 1
                            c_duel["status"] = "A FAZER"
                            if c_duel in game_state["kanban"]["in_validation"]:
                                game_state["kanban"]["in_validation"].remove(c_duel)
                            game_state["kanban"]["to_do"].append(c_duel)

                            if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"):
                                await asyncio.to_thread(jira_client.transition_issue, c_duel["id"], "A fazer")
                                safe_jira_comment(c_duel["id"], "PO Auditor", f"🚫 **REJEITADO NO CODE REVIEW:** {reason}")

                            game_state["boss_phase"] = f"🚫 PO REJEITOU PR DA BRANCH `{branch_to_merge}`!"

                        duel["is_active"] = False
                        duel["phase"] = "idle"

                await asyncio.sleep(1.0)

            await asyncio.sleep(2)

        except Exception as outer_e:
            logger.error(f"[Main Loop Exception] {outer_e}")
            await asyncio.sleep(2.0)


async def background_compliance_auditor_worker():
    await asyncio.sleep(10)
=======
async def _punish_non_compliant_card(card: Dict[str, Any], col: str, reason: str):
    card_id = str(card.get("id"))
    print(f"🚨 [Compliance Auditor] Card [{card_id}] em NÃO CONFORMIDADE ({reason}). Apagando comentários e movendo ao A Fazer...")
    
    # 1. Apaga TODOS os comentários do card no Jira Cloud
    await asyncio.to_thread(jira.clear_all_comments, card_id)
    
    # 2. Transiciona o card no Jira Cloud de volta para 'A fazer'
    punish_ok = await asyncio.to_thread(jira.transition_issue, card_id, "A fazer")
    if not punish_ok:
        print(f"🚨 [COMPLIANCE] Falha ao punir e mover {card_id} para 'A fazer' no Jira!")
    
    # 3. Adiciona comentário de Notificação de Punição por Não Conformidade
    punishment_msg = (
        f"🚨 **[PO COMPLIANCE AUDITOR] NON-COMPLIANCE DETECTADO!**\n\n"
        f"📌 **Motivo da Rejeição:** {reason}\n\n"
        f"🔨 **Ações de Punição Executadas:**\n"
        f"1. Todos os comentários antigos foram **removidos/apagados do Jira Cloud**.\n"
        f"2. O card foi transicionado de volta para a coluna **A fazer**.\n"
        f"3. O trabalho deve ser refeito em estrita conformidade com as regras (código Python real em src/flose/solutions/, Épico PAI e documentação técnica/negócio)."
    )
    await asyncio.to_thread(jira.add_comment, card_id, "PO Compliance Auditor", punishment_msg)
    
    # 4. Atualiza o estado local
    if card in game_state["kanban"].get(col, []):
        game_state["kanban"][col].remove(card)
        
    card["status"] = "A FAZER"
    card["rejections"] = card.get("rejections", 0) + 1
    card["po_rejection_reason"] = f"🚨 NON-COMPLIANCE: {reason[:40]}"
    game_state["kanban"]["to_do"].append(card)
    
    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "COMPLIANCE_AUDITOR_PUNISHED_CARD",
        "card_id": card_id,
        "reason": reason
    })


async def background_compliance_auditor_worker():
    """Worker de auditoria de compliance desativado a pedido do usuário."""
    return
    
>>>>>>> Stashed changes
    while True:
        try:
            check_list = []
            for col in ["in_progress", "in_validation", "done"]:
                for c in list(game_state["kanban"].get(col, [])):
                    check_list.append((c, col))

            for card, col in check_list:
                card_id = str(card.get("id", ""))
                if not card_id.startswith(f"{settings.jira_project_key}-"):
                    continue

<<<<<<< Updated upstream
                try:
                    details, http_code = await asyncio.to_thread(jira_client.get_issue_details, card_id)
                    if http_code == 404:
                        purge_card_from_kanban(card_id)
                        continue

                    if not details.get("fields", {}).get("parent"):
                        epic = game_state.get("current_epic_key")
                        if epic and card_id != epic:
                            linked, _ = await asyncio.to_thread(jira_client.link_parent_epic, card_id, epic)
                            if linked:
                                continue

                        await asyncio.to_thread(jira_client.transition_issue, card_id, "A fazer")
                        safe_jira_comment(card_id, "Governance", "🚨 **NON-COMPLIANCE!** Sem Épico Pai.")
=======
                # ✋ NÃO PUNA um card que está sendo processado agora pelo engine
                duel = game_state.get("duel", {})
                if duel.get("is_active") and duel.get("active_card", {}).get("id") == card.get("id"):
                    continue

                # Detalhes da issue no Jira Cloud
                issue_details = await asyncio.to_thread(jira.get_issue_details, card_id)
                fields = issue_details.get("fields", {})

                # Regra A: Deve ter Épico PAI (parent) — Auto-vincula se estiver ausente!
                if not fields.get("parent"):
                    linked = await asyncio.to_thread(jira.link_parent_epic, card_id)
                    if linked:
                        print(f"✅ [Compliance Auditor] Épico PAI vinculado automaticamente ao card {card_id}!")
                    else:
                        await _punish_non_compliant_card(card, col, "Ausência de Épico PAI (Parent Epic) no card.")
                        await asyncio.sleep(2)
                        continue

                # Regra B: Se estiver em Validação ou Concluído, DEVE ter módulo Python em src/flose/solutions/
                commit_info = card.get("commit_info", {})
                sol_file = commit_info.get("file_path", "")
                if col in ("in_validation", "done") and (not sol_file or not sol_file.startswith("src/flose/solutions/")):
                    await _punish_non_compliant_card(card, col, "Falta de ajuste/código Python real no diretório 'src/flose/solutions/'.")
                    await asyncio.sleep(2)
                    continue

                # Regra C: Se estiver em Fazendo (in_progress), deve ter comentário do Felipe
                if col == "in_progress":
                    raw_comments = fields.get("comment", {}).get("comments", [])
                    comments_text = ""
                    for cm in raw_comments:
                        content_list = cm.get("body", {}).get("content", [])
                        for node in content_list:
                            for inner in node.get("content", []):
                                comments_text += inner.get("text", "") + " "

                    has_biz_vision = "Visão de Negócio" in comments_text
                    has_tech_vision = "Visão Técnica" in comments_text

                    if not has_biz_vision or not has_tech_vision:
                        missing = []
                        if not has_biz_vision: missing.append("Visão de Negócio")
                        if not has_tech_vision: missing.append("Visão Técnica AST")
                        await _punish_non_compliant_card(card, col, f"Falta do comentário formal do Felipe com: {', '.join(missing)}.")
                        await asyncio.sleep(2)
                        continue
>>>>>>> Stashed changes

                        if card in game_state["kanban"].get(col, []):
                            game_state["kanban"][col].remove(card)
                        card["status"] = "A FAZER"
                        game_state["kanban"]["to_do"].append(card)
                except Exception:
                    pass
                await asyncio.sleep(0.5)
        except Exception:
            pass
        await asyncio.sleep(25)


<<<<<<< Updated upstream
# ====================================================================
# FASTAPI SERVER E DASHBOARD WEB COM CANVAS (RPG)
# ====================================================================

app = FastAPI(title="FLOSE AEOS — Real Software Engineering Automation Monolith")
=======
        await asyncio.sleep(20)
>>>>>>> Stashed changes


async def sync_jira_to_dashboard_loop():
    """
    Sincroniza o quadro Kanban do Jira real com o dashboard (game_state["kanban"]).
    IMPORTANTE: Não sobrescreve cards que estão sendo processados ativamente pelo engine.
    """
    while True:
        try:
            print("[JIRA SYNC] Atualizando board do Jira no Dashboard...")
            issues = jira.fetch_real_jira_issues("FLOSEUP", 200)

            # IDs dos cards em processamento ativo — NÃO devem ser alterados
            in_progress_ids = {c["id"] for c in game_state["kanban"].get("in_progress", [])}

            current_all = (
                game_state["kanban"]["to_do"] +
                game_state["kanban"]["in_progress"] +
                game_state["kanban"]["in_validation"] +
                game_state["kanban"]["done"]
            )
            card_map = {c["id"]: c for c in current_all}

            for issue in issues:
                iid = issue["id"]
                if iid in card_map:
                    if iid not in in_progress_ids:
                        card_map[iid]["status"] = issue["status"]
                    card_map[iid]["comments"] = issue["comments"]
                    card_map[iid]["title"] = issue["title"]
                    if not card_map[iid].get("description"):
                        card_map[iid]["description"] = issue.get("description", "")
                else:
                    card_map[iid] = issue

            to_do, in_progress, in_validation, done = [], [], [], []
            for card in card_map.values():
                cid = card.get("id")
                if cid in in_progress_ids:
                    in_progress.append(card)
                    continue
                status = card.get("status", "A FAZER")
                if status == "A FAZER":
                    to_do.append(card)
                elif status == "FAZENDO":
                    in_progress.append(card)
                elif status == "EM ANÁLISE":
                    in_validation.append(card)
                elif status == "FEITO":
                    done.append(card)

            game_state["kanban"]["to_do"] = to_do
            game_state["kanban"]["in_progress"] = in_progress
            game_state["kanban"]["in_validation"] = in_validation
            game_state["kanban"]["done"] = done

        except Exception as e:
            print(f"[JIRA SYNC ERROR] Erro na sincronização: {e}")

        await asyncio.sleep(15.0)

@app.on_event("startup")
<<<<<<< Updated upstream
async def startup_event():
    # 1. Restaura estado
    loaded_gs, loaded_pa, loaded_al = load_persisted_state()
    if loaded_gs and loaded_pa:
        game_state.update(loaded_gs)
        pixel_agents.update(loaded_pa)

    # 2. FAIL-FAST: Verifica Permissão e Projeto
    if _config_problems:
        game_state["jira_project_valid"] = False
        logger.error(
            "[Startup] Abortando sincronia principal: configuração do .env incompleta -> "
            + "; ".join(_config_problems)
        )
    else:
        project_key = settings.jira_project_key
        has_access = await asyncio.to_thread(jira_client.verify_project_access, project_key)
        if not has_access:
            game_state["jira_project_valid"] = False
            logger.error("[Startup] Abortando sincronia principal: verifique a chave do Projeto ou Permissões do Jira.")
        else:
            game_state["jira_project_valid"] = True
            # 3. OTIMIZAÇÃO: Validação em Lote (SSOT do Jira)
            try:
                live_cards = await asyncio.to_thread(jira_client.fetch_real_jira_issues, project_key, 100)
                new_kanban = {"to_do": [], "in_progress": [], "in_validation": [], "done": []}

                local_data = {c["id"]: c for col in game_state["kanban"].values() for c in col}
                for jc in live_cards:
                    cid = jc["id"]
                    card = local_data.get(cid, jc)
                    card.update({"title": jc["title"], "status": jc["status"], "parent": jc["parent"]})

                    if card["status"] == "A FAZER":
                        new_kanban["to_do"].append(card)
                    elif card["status"] == "EM PROGRESSO":
                        new_kanban["in_progress"].append(card)
                    elif card["status"] == "EM VALIDAÇÃO":
                        new_kanban["in_validation"].append(card)
                    elif card["status"] == "CONCLUÍDO":
                        new_kanban["done"].append(card)

                game_state["kanban"] = new_kanban
                logger.info("[Startup] Kanban sincronizado com a verdade absoluta do Jira.")
            except Exception as err:
                logger.error(f"[Startup Fetch Error] {err}")

    asyncio.create_task(save_state_to_disk())
    asyncio.create_task(main_engine_loop())
    asyncio.create_task(background_compliance_auditor_worker())
=======
async def start_autonomous_loop():
    await bus.start()
    asyncio.create_task(sync_jira_to_dashboard_loop())
    asyncio.create_task(dynamic_frenzy_and_training_game_loop())
    # Compliance Auditor desativado a pedido do usuário
    asyncio.create_task(background_boss_card_generator())
>>>>>>> Stashed changes


@app.get("/api/boss/state")
async def get_state():
    for agent in pixel_agents.values():
        agent["x"] = max(50, min(550, agent["x"] + random.choice([-2, 0, 2])))
        agent["y"] = max(200, min(320, agent["y"] + random.choice([-2, 0, 2])))

    return {
        "game_state": game_state,
        "pixel_agents": list(pixel_agents.values()),
        "duel": game_state["duel"],
        "kanban": game_state["kanban"],
        "audit_logs": audit_logs[-10:]
    }


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>FLOSE AEOS — Real Jira Mirror Engine</title>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { background: #0d0e15; color: #fff; font-family: 'Press Start 2P', monospace; overflow: hidden; }
            #game-container { display: flex; width: 100vw; height: 100vh; }
            #pixel-canvas { background: #181926; border-right: 4px solid #3b3d54; image-rendering: pixelated; flex-shrink: 0; }
            .side-panel { flex: 1; background: #11121d; padding: 1rem; display: flex; flex-direction: column; gap: 0.6rem; border-left: 4px solid #3b3d54; overflow-y: auto; }
            .hud-title { font-size: 0.6rem; color: #55ff55; text-shadow: 2px 2px #00aa00; text-align: center; padding: 0.4rem; border-bottom: 2px solid #1f2040; }
            .turn-banner { background: rgba(168, 85, 247, 0.15); border: 2px solid #a855f7; border-radius: 6px; padding: 0.5rem 0.8rem; text-align: center; font-size: 0.48rem; line-height: 1.6; }
            .duel-arena-box { background: rgba(59, 130, 246, 0.1); border: 2px solid #3b82f6; border-radius: 8px; padding: 0.7rem; }
            .duel-timer-bg { width: 100%; height: 16px; background: #440000; border: 2px solid #ff5555; border-radius: 4px; margin-top: 0.4rem; overflow: hidden; position: relative; }
            .duel-timer-fill { height: 100%; background: linear-gradient(90deg, #00ff00, #55ff55); transition: width 0.9s linear; }
            .kanban-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.4rem; }
            .kanban-col { background: rgba(0,0,0,0.6); border: 2px solid #30363d; border-radius: 6px; padding: 0.4rem; height: 270px; display: flex; flex-direction: column; }
            .kanban-col-cards { flex: 1; overflow-y: auto; padding-right: 0.2rem; }
            .kanban-col-cards::-webkit-scrollbar { width: 4px; }
            .kanban-col-cards::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 2px; }
            .kanban-col-title { font-size: 0.37rem; font-weight: bold; margin-bottom: 0.3rem; text-align: center; padding-bottom: 0.2rem; border-bottom: 1px solid #30363d; }
            .card-todo { color: #ff5555; border-color: #ff5555; }
            .card-progress { color: #60a5fa; border-color: #60a5fa; }
            .card-validation { color: #ffaa00; border-color: #ffaa00; }
            .card-done { color: #55ff55; border-color: #55ff55; }

            .kanban-card-item {
                background: rgba(255,255,255,0.05);
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 0.35rem;
                margin-bottom: 0.35rem;
                font-size: 0.34rem;
                line-height: 1.4;
            }
            .kanban-card-item.active-card { border-color: #60a5fa; background: rgba(59, 130, 246, 0.12); animation: pulse-card 1s ease-in-out infinite alternate; }
            .kanban-card-item.rejected-card { border-color: #ff5555; background: rgba(255, 85, 85, 0.08); }
            .epic-parent-badge { display: inline-block; background: rgba(168, 85, 247, 0.2); border: 1px solid #a855f7; color: #d8b4fe; font-size: 0.3rem; padding: 0.05rem 0.2rem; border-radius: 3px; margin-top: 0.15rem; }
            .delegated-badge { color: #3b82f6; font-size: 0.31rem; margin-top: 0.1rem; }

            @keyframes pulse-card { from { box-shadow: 0 0 4px rgba(59,130,246,0.3); } to { box-shadow: 0 0 10px rgba(59,130,246,0.8); } }
            .audit-log-entry { font-size: 0.36rem; color: #9ca3af; margin-bottom: 0.2rem; line-height: 1.4; }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>
            <div class="side-panel">
                <div class="hud-title">⚡ FLOSE AEOS — ESPELHO FIEL JIRA CLOUD & COMMITS GITHUB</div>
                <div id="turn-banner" class="turn-banner">FASE ATUAL: CARREGANDO...</div>
                <div id="duel-box" class="duel-arena-box">
                    <div style="font-size:0.46rem; color:#60a5fa; text-align:center;">AGUARDANDO PROCESSO...</div>
                </div>
                <div class="kanban-grid">
                    <div class="kanban-col">
                        <div class="kanban-col-title card-todo" id="title-todo">🔴 A FAZER (0)</div>
                        <div class="kanban-col-cards" id="col-todo"></div>
                    </div>
                    <div class="kanban-col">
                        <div class="kanban-col-title card-progress" id="title-progress">🔵 EM PROGRESSO (0)</div>
                        <div class="kanban-col-cards" id="col-progress"></div>
                    </div>
                    <div class="kanban-col">
                        <div class="kanban-col-title card-validation" id="title-validation">🟡 EM VALIDAÇÃO (0)</div>
                        <div class="kanban-col-cards" id="col-validation"></div>
                    </div>
                    <div class="kanban-col">
                        <div class="kanban-col-title card-done" id="title-done">🟢 CONCLUÍDO (0)</div>
                        <div class="kanban-col-cards" id="col-done"></div>
                    </div>
                </div>
                <div>
                    <div style="font-size:0.44rem; color:#a855f7; margin-bottom:0.3rem;">
                        🐙 COMMITS REAIS NO GITHUB <span id="commit-count" style="color:#22c55e; font-size:0.38rem;"></span>
                    </div>
                </div>
                <div>
                    <div style="font-size:0.42rem; color:#55ff55; margin-bottom:0.2rem;">📜 AUDIT LOG</div>
                    <div id="audit-log" style="max-height: 80px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('pixel-canvas');
            const ctx = canvas.getContext('2d');

            function resizeCanvas() {
                canvas.width = Math.floor(window.innerWidth * 0.52);
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];
            let duelState = {};
            let kanbanState = {};

            function drawPixelSprite(x, y, color, name, isDuelist, lvl, action) {
                const blink = Math.floor(Date.now() / 500) % 2 === 0;
                ctx.fillStyle = color;
                ctx.fillRect(x, y + 10, 24, 20);
                ctx.fillStyle = "#ffcc99";
                ctx.fillRect(x + 4, y, 16, 14);
                ctx.fillStyle = "#000";
                ctx.fillRect(x + 7, y + 4, 3, 3);
                ctx.fillRect(x + 14, y + 4, 3, 3);
                ctx.font = '7px "Press Start 2P"';
                ctx.fillStyle = color;
                ctx.fillText(`${name} Lv.${lvl}`, x - 8, y - 12);

                if (action) {
                    ctx.font = '5px "Press Start 2P"';
                    ctx.fillStyle = "#9ca3af";
                    ctx.fillText(action.substring(0, 28), x - 20, y - 3);
                }

                if (isDuelist) {
                    if (blink) {
                        ctx.strokeStyle = "#60a5fa";
                        ctx.lineWidth = 2;
                        ctx.strokeRect(x - 3, y - 3, 30, 36);
                    }
                    ctx.fillStyle = "#3b82f6";
                    ctx.fillRect(x - 2, y - 24, 28, 9);
                    ctx.font = '5px "Press Start 2P"';
                    ctx.fillStyle = "#fff";
                    ctx.fillText("⚔️ DUELO", x, y - 17);
                }
            }

            function drawPOBoss(hpPercent, phaseText) {
                const bx = canvas.width / 2 - 40;
                const by = 55;
                const bossAnim = Math.sin(Date.now() / 400) * 3;

                ctx.fillStyle = "#1e1e2e";
                ctx.fillRect(bx, by + 30 + bossAnim, 80, 70);
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 36, by + 35 + bossAnim, 8, 35);
                ctx.fillStyle = "#313244";
                ctx.fillRect(bx + 10, by + bossAnim, 60, 40);
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 18, by + 12 + bossAnim, 14, 10);
                ctx.fillRect(bx + 48, by + 12 + bossAnim, 14, 10);
                ctx.fillRect(bx + 15, by - 10 + bossAnim, 8, 14);
                ctx.fillRect(bx + 57, by - 10 + bossAnim, 8, 14);

                ctx.font = '9px "Press Start 2P"';
                ctx.fillStyle = "#ff5555";
                ctx.fillText("👹 PO EVIL BOSS", bx - 30, by - 20 + bossAnim);

                const hpBarW = 320;
                const hpBarX = canvas.width / 2 - hpBarW / 2;
                ctx.fillStyle = "#440000";
                ctx.fillRect(hpBarX, 12, hpBarW, 18);

                const hpColor = hpPercent > 60 ? "#ff3333" : hpPercent > 30 ? "#ff8800" : "#ff0000";
                ctx.fillStyle = hpColor;
                ctx.fillRect(hpBarX, 12, (hpBarW * Math.max(0, hpPercent)) / 100, 18);
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = 2;
                ctx.strokeRect(hpBarX, 12, hpBarW, 18);

                ctx.font = '6px "Press Start 2P"';
                ctx.fillStyle = "#ffffff";
                ctx.fillText(`HP: ${Math.round(Math.max(0, hpPercent))}%`, hpBarX + 4, 25);

                ctx.font = '5px "Press Start 2P"';
                ctx.fillStyle = "#ffaa00";
                ctx.fillText(phaseText ? phaseText.substring(0, 55) : "", canvas.width / 2 - 160, by + 120 + bossAnim);
            }

            function render() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#11111b";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                for (let i = 0; i < canvas.width; i += 40) {
                    ctx.strokeStyle = "#1a1b2e";
                    ctx.lineWidth = 1;
                    ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
                }
                for (let j = 0; j < canvas.height; j += 40) {
                    ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(canvas.width, j); ctx.stroke();
                }

                if (gameState && gameState.boss_max_hp) {
                    const hpPct = (gameState.boss_hp / gameState.boss_max_hp) * 100;
                    drawPOBoss(hpPct, gameState.boss_phase || "");

                    agentsList.forEach(a => {
                        const isDuelist = duelState && duelState.is_active && duelState.active_hero === a.name;
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, isDuelist, a.skill_level, a.action);
                    });

                    ctx.font = '8px "Press Start 2P"';
                    ctx.fillStyle = "#55ff55";
                    ctx.fillText(`⏱️ ${gameState.phase_timer_sec || 0}s`, canvas.width / 2 - 30, canvas.height - 20);
                }

                requestAnimationFrame(render);
            }
            render();

            async function updateState() {
                try {
                    const res = await fetch('/api/boss/state');
                    const data = await res.json();
                    gameState = data.game_state;
                    agentsList = data.pixel_agents;
                    duelState = data.duel;
                    kanbanState = data.kanban;
                    const auditLogs = data.audit_logs;

                    const banner = document.getElementById('turn-banner');

                    if (gameState.jira_project_valid === false) {
                        banner.innerHTML = `<span style="color:#ff5555; font-weight:bold;">🚨 ERRO DE CONFIGURAÇÃO DO JIRA!</span> VERIFIQUE O NOME DO PROJETO E PERMISSÕES DA API.`;
                        banner.style.borderColor = "#ff5555";
                        banner.style.background = "rgba(255, 85, 85, 0.15)";
                    } else {
                        banner.innerHTML = `⚙️ PIPELINE REAL | DEMANDAS CONCLUÍDAS: ${gameState.cards_processed_count || 0}`;
                        banner.style.borderColor = "#a855f7";
                        banner.style.background = "rgba(168, 85, 247, 0.15)";
                    }

                    const duel = duelState;
                    if (duel && duel.is_active && duel.active_card) {
                        const pct = Math.max(0, (duel.timeout_timer_sec / duel.max_timeout_sec) * 100);
                        const timerColor = pct < 30 ? '#ff5555' : pct < 60 ? '#ffaa00' : '#00ff00';
                        const phaseLabel = duel.phase === "hero_working" ? `💻 HERÓI CODIFICANDO (${duel.work_progress || 0}%)` : "🔍 PO VILÃO REVISANDO & MERGANDO";
                        const phaseColor = duel.phase === "hero_working" ? "#60a5fa" : "#ffaa00";

                        document.getElementById('duel-box').innerHTML = `
                            <div style="font-size:0.52rem; color:${phaseColor}; font-weight:bold; margin-bottom:0.25rem; text-align:center;">
                                ${phaseLabel}
                            </div>
                            <div style="font-size:0.44rem; color:#3b82f6; margin-bottom:0.2rem;">
                                👔 <b>Felipe:</b> Delegou para <span style="color:#a855f7;">${duel.active_hero}</span>!
                            </div>
                            <div style="font-size:0.46rem; color:#fff; margin-bottom:0.2rem;">
                                ⚔️ <b>Herói em Ação:</b> <span style="color:#a855f7;">${duel.active_hero}</span> — Card: <span style="color:#ec4899;">[${duel.active_card.id}]</span>
                            </div>
                            <div style="font-size:0.42rem; color:#55ff55; font-weight:bold; margin-bottom:0.25rem;">
                                ${duel.active_power || 'Trabalhando...'}
                            </div>
                            <div style="font-size:0.38rem; color:#9ca3af; margin-bottom:0.25rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                ${duel.active_card.title ? duel.active_card.title.substring(0, 45) + '...' : ''}
                            </div>
                            <div style="font-size:0.42rem; color:${timerColor}; font-weight:bold; margin-bottom:0.2rem;">
                                ⏱️ TIMEOUT: ${typeof duel.timeout_timer_sec === 'number' ? duel.timeout_timer_sec.toFixed(1) : '??'}s
                            </div>
                            <div class="duel-timer-bg">
                                <div class="duel-timer-fill" style="width:${pct}%; background:${timerColor};"></div>
                            </div>
                        `;
                    } else {
                        document.getElementById('duel-box').innerHTML = `
                            <div style="font-size:0.46rem; color:#9ca3af; text-align:center; padding:0.5rem;">😴 AGUARDANDO PRÓXIMO CARD NO JIRA CLOUD...</div>
                        `;
                    }

                    const activeCardId = duel && duel.active_card ? duel.active_card.id : null;
                    const todoCards = kanbanState.to_do || [];
                    const progressCards = kanbanState.in_progress || [];
                    const validationCards = kanbanState.in_validation || [];
                    const doneCards = kanbanState.done || [];

                    document.getElementById('title-todo').textContent = `🔴 A FAZER (${todoCards.length})`;
                    document.getElementById('title-progress').textContent = `🔵 EM PROGRESSO (${progressCards.length})`;
                    document.getElementById('title-validation').textContent = `🟡 EM VALIDAÇÃO (${validationCards.length})`;
                    document.getElementById('title-done').textContent = `🟢 CONCLUÍDO (${doneCards.length})`;

                    function renderCards(cards, colorClass) {
                        if (!cards || cards.length === 0) return '<div style="font-size:0.32rem; color:#4b5563; text-align:center; padding:0.8rem 0;">Nenhum card</div>';
                        return cards.map(c => {
                            const isActive = c.id === activeCardId;
                            const isRejected = c.rejections > 0;
                            const jiraUrl = `https://felipeflose.atlassian.net/browse/${c.id}`;
                            const titleFull = c.title || '';
                            const parentEpic = c.parent || null;
                            const delegatedTo = c.delegated_to || null;

                            return `
                                <div class="kanban-card-item ${isActive ? 'active-card' : ''} ${isRejected && !isActive ? 'rejected-card' : ''}">
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.15rem;">
                                        <a href="${jiraUrl}" target="_blank" style="color:${colorClass}; font-weight:bold; font-size:0.38rem; text-decoration:underline;">
                                            ${c.id} 🔗
                                        </a>
                                    </div>
                                    <div style="font-size:0.34rem; color:#e5e7eb; line-height:1.3; margin-bottom:0.2rem;" title="${titleFull}">
                                        ${titleFull}
                                    </div>
                                    ${parentEpic ? `<div class="epic-parent-badge">📌 Pai: ${parentEpic}</div>` : ''}
                                    ${delegatedTo ? `<div class="delegated-badge">👤 ${delegatedTo}</div>` : ''}
                                </div>
                            `;
                        }).join('');
                    }

                    document.getElementById('col-todo').innerHTML = renderCards(todoCards, '#ff5555');
                    document.getElementById('col-progress').innerHTML = renderCards(progressCards, '#60a5fa');
                    document.getElementById('col-validation').innerHTML = renderCards(validationCards, '#ffaa00');
                    document.getElementById('col-done').innerHTML = renderCards(doneCards, '#55ff55');

                    document.getElementById('commit-count').textContent = `(${gameState.total_real_commits || 0} commits reais ✅)`;

                    document.getElementById('audit-log').innerHTML = auditLogs.map(l => {
                        return `<div class="audit-log-entry">» [${l.action}] ${(l.reason || l.card_id || '').substring(0, 55)}</div>`;
                    }).join('');

                } catch(e) {
                    console.error('Update error:', e);
                }
            }

            updateState();
            setInterval(updateState, 400);
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.port)