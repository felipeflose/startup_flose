import asyncio
import time
import random
import os
import sys
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

os.makedirs(SOLUTIONS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(SKILLS_DOC_PATH), exist_ok=True)
os.makedirs(os.path.dirname(PERSISTENCE_FILE), exist_ok=True)


# ====================================================================
# CONFIGURAÇÃO CENTRALIZADA
# ====================================================================

class Settings:
    def __init__(self):
        raw_host = (
            os.getenv("JIRA_HOST")
            or os.getenv("JIRA_DOMAIN")
            or "https://felipeflose.atlassian.net"
        )
        self.jira_domain = raw_host.replace("https://", "").replace("http://", "").rstrip("/")

        self.jira_email = os.getenv("JIRA_USER") or os.getenv("JIRA_EMAIL") or ""
        self.jira_api_token = os.getenv("JIRA_TOKEN") or os.getenv("JIRA_API_TOKEN") or ""
        self.jira_project_key = os.getenv("JIRA_PROJECT_KEY", "FLOSEUP")

        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.github_owner = os.getenv("GITHUB_OWNER", "")
        self.github_repo = os.getenv("GITHUB_REPO", "")

        self.port = int(os.getenv("PORT", "8085"))

        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "gemma4-fast:latest")
        self.ollama_code_model = os.getenv("OLLAMA_CODE_MODEL", "qwen2.5-coder:latest")

    def validate(self) -> List[str]:
        problems = []
        if not self.jira_domain: problems.append("JIRA_HOST/JIRA_DOMAIN não definido no .env")
        if not self.jira_email: problems.append("JIRA_USER/JIRA_EMAIL não definido no .env")
        if not self.jira_api_token: problems.append("JIRA_TOKEN/JIRA_API_TOKEN não definido no .env")
        return problems

settings = Settings()
_config_problems = settings.validate()
if _config_problems:
    for problem in _config_problems: logger.warning(f"[Config] {problem}")


# ====================================================================
# CLIENTE HTTP NATIVO DA API REST V3 DO JIRA CLOUD
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
            if http_err.code != 404: logger.error(f"[Jira HTTP Error {http_err.code}] {endpoint}: {err_body}")
            return http_err.code, {"error": err_body}
        except Exception as ex:
            return 500, {"error": str(ex)}

    def verify_project_access(self, project_key: str) -> bool:
        status_code, _ = self._request("GET", f"/project/{project_key}")
        return status_code == 200

    def fetch_real_jira_issues(self, project_key: str = None, limit: int = 150) -> List[Dict[str, Any]]:
        project_key = project_key or settings.jira_project_key
        jql = f"project = {project_key} AND issuetype not in (Epic, Épico) ORDER BY updated DESC"
        endpoint = "/search/jql"
        payload = {"jql": jql, "maxResults": limit, "fields": ["summary", "description", "status", "parent", "created"]}
        status_code, response_data = self._request("POST", endpoint, payload)
        if status_code != 200 or "issues" not in response_data: return []

        parsed_cards = []
        for issue in response_data.get("issues", []):
            key = issue.get("key")
            fields = issue.get("fields", {})
            parent_key = fields.get("parent", {}).get("key") if fields.get("parent") else None
            raw_description = self._parse_adf_document(fields.get("description"))
            raw_status = fields.get("status", {}).get("name", "A Fazer").upper()

            parsed_cards.append({
                "id": str(key), "title": fields.get("summary", f"Issue {key}"),
                "description": raw_description if raw_description else "Sem descrição registrada.",
                "status": self._normalize_jira_status(raw_status), "parent": parent_key,
                "rejections": 0, "created_at": fields.get("created", datetime.now().isoformat()), "is_real_jira": True
            })
        return parsed_cards

    def create_detailed_epic_or_task(self, project_key: str, summary: str, description: str, epic_name: Optional[str] = None) -> Dict[str, Any]:
        type_candidates = ["Epic", "Épico"] if epic_name else ["Task", "Tarefa", "Story", "História"]
        for itype in type_candidates:
            payload = {
                "fields": {
                    "project": {"key": project_key}, "summary": summary,
                    "description": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]},
                    "issuetype": {"name": itype}
                }
            }
            status_code, body = self._request("POST", "/issue", payload)
            if status_code in (200, 201) and "key" in body: return {"key": body["key"], "success": True}
        return {"key": None, "success": False, "error": "Incapaz de criar item."}

    def link_parent_epic(self, issue_key: str, epic_key: str) -> Tuple[bool, int]:
        if not issue_key or not epic_key or issue_key == epic_key: return False, 400
        payload = {"fields": {"parent": {"key": epic_key}}}
        status_code, _ = self._request("PUT", f"/issue/{issue_key}", payload)
        return status_code in (200, 204), status_code

    def transition_issue(self, issue_key: str, target_status_name: str) -> Tuple[bool, int]:
        status_code, data = self._request("GET", f"/issue/{issue_key}/transitions")
        if status_code != 200 or "transitions" not in data: return False, status_code
        target_norm = target_status_name.lower().strip()
        selected_transition_id = next((t.get("id") for t in data["transitions"] if target_norm in (t.get("name", "").lower(), t.get("to", {}).get("name", "").lower())), None)
        if not selected_transition_id: return False, 400
        payload = {"transition": {"id": selected_transition_id}}
        post_status, _ = self._request("POST", f"/issue/{issue_key}/transitions", payload)
        return post_status in (200, 204), post_status

    def add_comment(self, issue_key: str, author_title: str, text: str) -> Tuple[bool, int]:
        payload = {
            "body": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": f"[{author_title}]: ", "marks": [{"type": "strong"}]}, {"type": "text", "text": text}]}]
            }
        }
        status_code, _ = self._request("POST", f"/issue/{issue_key}/comment", payload)
        return status_code in (200, 201), status_code

    def get_issue_details(self, issue_key: str) -> Tuple[Dict[str, Any], int]:
        status_code, data = self._request("GET", f"/issue/{issue_key}?fields=summary,description,status,parent,comment")
        return data if status_code == 200 else {}, status_code

    def _parse_adf_document(self, adf_node: Any) -> str:
        if not adf_node or not isinstance(adf_node, dict): return ""
        extracted = []
        def _walk(node):
            if isinstance(node, dict):
                if node.get("type") == "text" and "text" in node: extracted.append(node["text"])
                for child in node.get("content", []): _walk(child)
            elif isinstance(node, list):
                for item in node: _walk(item)
        _walk(adf_node)
        return " ".join(extracted).strip()

    def _normalize_jira_status(self, raw_status: str) -> str:
        s = raw_status.upper()
        if any(term in s for term in ["PROGRESS", "FAZENDO", "IN WORK"]): return "EM PROGRESSO"
        if any(term in s for term in ["VALIDA", "ANALISE", "REVIEW"]): return "EM VALIDAÇÃO"
        if any(term in s for term in ["DONE", "FEITO", "CONCLU"]): return "CONCLUÍDO"
        return "A FAZER"


# ====================================================================
# CLIENTE LLM LOCAL (OLLAMA)
# ====================================================================

class LocalLLMClient:
    def __init__(self):
        self.host = settings.ollama_host
        self.model = settings.ollama_model
        self.code_model = settings.ollama_code_model
        self.chat_url = f"{self.host}/api/chat"

    def _call(self, system_prompt: str, user_prompt: str, model: Optional[str] = None) -> Optional[str]:
        payload = {
            "model": model or self.model, "stream": False, "format": "json",
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.chat_url, data=body_bytes, method="POST", headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("message", {}).get("content", "").strip() or None
        except Exception: return None

    @staticmethod
    def _extract_json(raw_text: str) -> Optional[Dict[str, Any]]:
        if not raw_text: return None
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip())
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try: return json.loads(cleaned)
        except Exception:
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                try: return json.loads(match.group(0))
                except Exception: pass
        return None

    def delegate_task_as_felipe(self, card_title: str, card_desc: str) -> Tuple[str, str]:
        system_prompt = (
            "Você é Felipe, Líder de Arquitetura. Analise a demanda e escolha o executor mais adequado.\n"
            "Regras: 'sofia' (IA/LLM/Parsing), 'lucas' (Backend/Async/BD), 'beatriz' (Testes/Segurança/Refatoração).\n"
            "Retorne APENAS um JSON estrito: {\"assigned\": \"<sofia|lucas|beatriz>\", \"reason\": \"<motivo curto>\"}"
        )
        user_prompt = f"Título: {card_title}\nDescrição: {card_desc}"
        raw = self._call(system_prompt, user_prompt)
        parsed = self._extract_json(raw) if raw else None
        if parsed and parsed.get("assigned") in ["sofia", "lucas", "beatriz"]: return parsed["assigned"], str(parsed.get("reason", ""))
        return "lucas", "Fallback de segurança."

    def extract_skill_from_card(self, card_title: str, card_desc: str) -> str:
        system_prompt = (
            "Você é um avaliador de habilidades técnicas. Leia a tarefa concluída e nomeie a habilidade adquirida de forma épica. "
            "Ex: '⚡ Async I/O Overdrive'. Retorne APENAS JSON: {\"power\": \"<nome da habilidade>\"}"
        )
        user_prompt = f"Título: {card_title}\nDescrição: {card_desc}"
        raw = self._call(system_prompt, user_prompt)
        parsed = self._extract_json(raw) if raw else None
        return parsed.get("power", "✨ Lógica Evoluída") if parsed else "✨ Lógica Evoluída"

    def generate_card_brief(self, project_context: str) -> Optional[Dict[str, str]]:
        system_prompt = (
            "Você é um PO. Crie UMA demanda técnica implementável em Python. Responda APENAS JSON: {\"title\": \"...\", \"description\": \"...\"}."
        )
        raw = self._call(system_prompt, f"Contexto: {project_context}\nCrie demanda.")
        parsed = self._extract_json(raw) if raw else None
        if parsed and parsed.get("title") and parsed.get("description"): return {"title": str(parsed["title"])[:120], "description": str(parsed["description"])[:800]}
        return None

    def generate_solution_stream(self, card_title: str, card_description: str, hero_name: str, hero_class: str, learned_skills: List[str], chunk_callback, check_cancel) -> Optional[str]:
        """Geração real via Stream. Se a IA estourar o limite, check_cancel interrompe o processo na força."""
        skills_context = ", ".join(learned_skills) if learned_skills else "Ainda não obteve habilidades especiais."
        system_prompt = (
            f"Você é {hero_name}, {hero_class}. Implemente a solução REAL.\n"
            f"🌟 SUAS HABILIDADES: {skills_context}.\n"
            "Retorne APENAS o código Python puro, cru. SEM formatar em markdown, SEM blocos ```python. Apenas código."
        )
        payload = {
            "model": self.code_model, "stream": True,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Card: {card_title}\nDescrição: {card_description}"}
            ]
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.chat_url, data=body_bytes, method="POST", headers={"Content-Type": "application/json"})
        
        full_code = ""
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                for line in resp:
                    # KILL SWITCH: Interrompe brutalmente a leitura se o tempo esgotou!
                    if check_cancel():
                        logger.warning(f"[KILL SWITCH ATIVADO] Abortando inferência forçadamente para {hero_name}!")
                        return None
                    
                    if line:
                        decoded = line.decode('utf-8').strip()
                        if decoded:
                            data = json.loads(decoded)
                            chunk = data.get("message", {}).get("content", "")
                            if chunk:
                                full_code += chunk
                                chunk_callback(chunk)
        except Exception as ex:
            logger.error(f"[Stream Error] {ex}")
            return None

        cleaned = re.sub(r"^```(?:python)?\s*", "", full_code.strip())
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned


local_llm_client = LocalLLMClient()


# ====================================================================
# ENGINE DE OPERAÇÕES DO GIT LOCAL
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
        if ret_code != 0 and "already exists" in stderr: await _exec_git(["checkout", branch_name])
        return True

async def git_commit_and_push(branch_name: str, file_path: str, commit_message: str) -> Tuple[bool, str, str]:
    async with _git_merge_lock:
        await _exec_git(["add", file_path])
        await _exec_git(["commit", "-m", commit_message])
        _, hash_out, _ = await _exec_git(["rev-parse", "--short", "HEAD"])
        push_code, _, push_err = await _exec_git(["push", "origin", branch_name])
        return push_code == 0, hash_out.strip() if hash_out else "HEAD", push_err

async def po_vilao_merge_and_delete_branch(branch_name: str) -> Tuple[bool, str]:
    if not branch_name or branch_name == "main": return True, "Sem branch."
    async with _git_merge_lock:
        try:
            await _exec_git(["fetch", "origin"])
            await _exec_git(["checkout", "main"])
            await _exec_git(["pull", "origin", "main"])
            target_ref = branch_name if (await _exec_git(["rev-parse", "--verify", branch_name]))[0] == 0 else f"origin/{branch_name}"
            merge_code, _, stderr = await _exec_git(["merge", target_ref, "--no-ff", "-m", f"chore(release): PO merged {branch_name} into main"])
            if merge_code != 0: return False, f"Falha no Git Merge: {stderr.strip()[:150]}"
            await _exec_git(["push", "origin", "main"])
            await _exec_git(["branch", "-D", branch_name])
            await _exec_git(["push", "origin", "--delete", branch_name])
            return True, f"🔀 Branch `{branch_name}` integrada e removida."
        except Exception as e: return False, f"Erro ao processar Merge no Git: {e}"


# ====================================================================
# EXECUTOR DE TESTES UNITÁRIOS COM PYTEST
# ====================================================================

def run_pytest(relative_file_path: str) -> Tuple[bool, str]:
    abs_path = os.path.join(REPO_PATH, relative_file_path)
    if not os.path.exists(abs_path): return False, "Arquivo não localizado no disco."
    try:
        res = subprocess.run([sys.executable, "-m", "pytest", abs_path, "-v", "--tb=short"], cwd=REPO_PATH, capture_output=True, text=True, timeout=60)
        passed = (res.returncode == 0)
        return passed, (res.stdout if passed else res.stderr)[:400]
    except subprocess.TimeoutExpired: return False, "Timeout: A suíte excedeu 30s."
    except Exception as ex: return False, f"Falha Pytest: {ex}"


# ====================================================================
# GERENCIAMENTO DE PERSISTÊNCIA E ESTADO
# ====================================================================

jira_client = JiraCloudConnector()

game_state: Dict[str, Any] = {
    "boss_name": "PO EVIL BOSS", "boss_hp": 1000, "boss_max_hp": 1000, "boss_stage": 1,
    "current_epic_key": None, "current_phase": "HERO_TRAINING_PHASE", "phase_timer_sec": 120,
    "target_cards_to_clear_80pct": 0, "cards_cleared_in_current_wave": 0, "victory": False,
    "boss_phase": "🎓 ACADEMIA DOS HERÓIS", "jira_project_valid": True,
    "duel": {
        "is_active": False, "active_hero": None, "hero_key": None, "active_card": None,
        "timeout_timer_sec": 150.0, "max_timeout_sec": 150.0,
        "active_power": "Idle", "phase": "idle", "last_code": "", "llm_finished": False, "commit_info": None,
        "kill_flag": False
    },
    "kanban": {"to_do": [], "in_progress": [], "in_validation": [], "done": []},
    "total_real_commits": 0, "cards_processed_count": 0
}

pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {"name": "Felipe", "class": "Líder de Arquitetura", "sprite_color": "#3b82f6", "x": 100, "y": 260, "skill_level": 1, "xp": 0, "action": "Router", "learned_skills": ["🧠 Visão de Arquitetura"]},
    "sofia": {"name": "Sofia", "class": "Especialista IA", "sprite_color": "#ec4899", "x": 220, "y": 220, "skill_level": 1, "xp": 0, "action": "Inferência Local", "learned_skills": ["✨ Fundamentos IA"]},
    "lucas": {"name": "Lucas", "class": "Eng. Backend", "sprite_color": "#f97316", "x": 350, "y": 270, "skill_level": 1, "xp": 0, "action": "Otimização de I/O", "learned_skills": ["⚙️ Clean Code Python"]},
    "beatriz": {"name": "Beatriz", "class": "Eng. QA & Security", "sprite_color": "#10b981", "x": 480, "y": 230, "skill_level": 1, "xp": 0, "action": "Cobertura Pytest", "learned_skills": ["🛡️ Defesa Anti-Bug"]}
}

audit_logs: List[Dict[str, Any]] = []

def purge_card_from_kanban(card_id: str):
    for col_name in ["to_do", "in_progress", "in_validation", "done"]:
        game_state["kanban"][col_name] = [c for c in game_state["kanban"].get(col_name, []) if str(c.get("id")) != str(card_id)]
    if game_state["duel"].get("active_card") and game_state["duel"]["active_card"].get("id") == card_id:
        game_state["duel"]["is_active"] = False
        game_state["duel"]["phase"] = "idle"

def load_persisted_state() -> Tuple[Optional[Dict], Optional[Dict], Optional[List]]:
    if os.path.exists(PERSISTENCE_FILE):
        try:
            with open(PERSISTENCE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("game_state"), data.get("pixel_agents"), data.get("audit_logs")
        except Exception: pass
    return None, None, None

async def save_state_to_disk():
    while True:
        await asyncio.sleep(3.0)
        try:
            with open(PERSISTENCE_FILE, "w", encoding="utf-8") as f:
                json.dump({"game_state": game_state, "pixel_agents": pixel_agents, "audit_logs": audit_logs[-50:]}, f, indent=2, ensure_ascii=False)
        except Exception: pass


# ====================================================================
# MECÂNICAS REAIS DE JOGO E GERAÇÃO 100% LLM DEPENDENT
# ====================================================================

async def felipe_analyze_and_delegate_card_async(card: Dict[str, Any]) -> str:
    assigned, reason = await asyncio.to_thread(local_llm_client.delegate_task_as_felipe, card.get("title", ""), card.get("description", ""))
    card["delegated_by"] = "Felipe (AI Router)"
    card["delegated_to"] = pixel_agents[assigned]["name"]
    card["delegation_note"] = reason
    return assigned

async def ensure_real_stage_epic_async(stage_num: int) -> Optional[str]:
    if game_state.get("current_epic_key"):
        _, status_code = await asyncio.to_thread(jira_client.get_issue_details, game_state["current_epic_key"])
        if status_code == 200: return game_state["current_epic_key"]
    summary = f"ÉPICO MASTER REFACTORING STAGE {stage_num}"
    jira_res = await asyncio.to_thread(jira_client.create_detailed_epic_or_task, settings.jira_project_key, summary, "Épico mestre.", summary)
    real_key = jira_res.get("key")
    if real_key:
        game_state["current_epic_key"] = real_key
        return real_key
    return None

async def synthesize_code_and_commit_stream(hero_name: str, hero_class: str, card_title: str, card_description: str, card_id: str, branch_name: str, learned_skills: List[str], chunk_handler, check_cancel) -> Dict[str, Any]:
    await git_checkout_and_create_branch(branch_name)
    safe_id = re.sub(r'[^a-zA-Z0-9_]', '_', card_id.lower())
    rel_path = os.path.join("src", "flose", "solutions", f"solution_{safe_id}.py")
    abs_path = os.path.join(REPO_PATH, rel_path)

    generated_code = await asyncio.to_thread(
        local_llm_client.generate_solution_stream, card_title, card_description or card_title, hero_name, hero_class, learned_skills, chunk_handler, check_cancel
    )
    
    if check_cancel() or not generated_code:
        # Se foi morto pela rule do Timeout, não subimos lixo no repositório.
        return {"success": False, "used_llm": False, "error": "Processo abortado (Killed pelo Timeout)."}
    
    python_code = f'"""\nSolução para [{card_id}]\nAutor: {hero_name}\nHabilidades Empregadas: {", ".join(learned_skills[-2:])}\n"""\n{generated_code}'

    with open(abs_path, "w", encoding="utf-8") as f: f.write(python_code)
    lines_added = len(python_code.splitlines())
    test_passed, test_out = run_pytest(rel_path)
    
    commit_msg = f"feat({card_id.lower()}): implement solution by {hero_name}"
    push_ok, commit_hash, err = await git_commit_and_push(branch_name, rel_path, commit_msg)

    return {
        "success": push_ok and test_passed, "commit_hash": commit_hash,
        "file_path": rel_path, "lines_added": lines_added,
        "test_passed": test_passed, "test_output": test_out,
        "used_llm": True, "error": err if not push_ok else None
    }

def inspect_commit_delivery(commit_info: Dict[str, Any]) -> Tuple[bool, str]:
    if not commit_info or not commit_info.get("success"): return False, "Falha na pipeline CI/Pytest ou Processo Interrompido."
    if commit_info.get("lines_added", 0) < 5: return False, "Código muito raso."
    return True, "Aprovado. Pipeline CI validou o .py."

def safe_jira_comment(card_id: str, author: str, text: str):
    asyncio.create_task(asyncio.to_thread(jira_client.add_comment, card_id, author, text))


# ====================================================================
# CICLO PRINCIPAL DO JOGO (MAIN LOOP)
# ====================================================================

async def main_engine_loop():
    await asyncio.sleep(2.0)
    while True:
        try:
            if not game_state.get("jira_project_valid", True):
                game_state["boss_phase"] = "🚫 FALHA: PROJETO JIRA INVÁLIDO!"
                await asyncio.sleep(5.0)
                continue

            stage = game_state.get("boss_stage", 1)
            master_epic_key = await ensure_real_stage_epic_async(stage)

            if game_state.get("victory") or game_state.get("boss_hp", 0) <= 0:
                stage += 1
                game_state["boss_stage"] = stage; game_state["boss_max_hp"] = 1000 + (stage * 500)
                game_state["boss_hp"] = game_state["boss_max_hp"]; game_state["boss_name"] = f"PO EVIL BOSS (STAGE {stage})"
                game_state["victory"] = False; game_state["current_epic_key"] = None
                game_state["boss_phase"] = f"🔥 PO VILÃO EVOLUIU PARA O ESTÁGIO {stage}!"
                await asyncio.sleep(3); continue

            backlog_size = len(game_state["kanban"]["to_do"])
            if backlog_size < 3:
                game_state["current_phase"] = "PO_FRENZY_30S"
                game_state["boss_phase"] = f"⚡ PO CRIANDO CARDS REAIS NO JIRA!"
                for _ in range(3 - backlog_size):
                    brief = await asyncio.to_thread(local_llm_client.generate_card_brief, "Automação engenharia Python.")
                    title = brief["title"] if brief else f"Demanda Automática #{random.randint(100, 999)}"
                    card_description = brief["description"] if brief else "LLM Timeout."
                    res = await asyncio.to_thread(jira_client.create_detailed_epic_or_task, settings.jira_project_key, title, card_description)
                    if res.get("key"):
                        if master_epic_key: await asyncio.to_thread(jira_client.link_parent_epic, res["key"], master_epic_key)
                        game_state["kanban"]["to_do"].append({
                            "id": res["key"], "title": title, "description": card_description,
                            "status": "A FAZER", "parent": master_epic_key, "rejections": 0, "is_real_jira": True
                        })
                await asyncio.sleep(2.0)

            target_clear = max(1, int(len(game_state["kanban"]["to_do"]) * 0.8))
            game_state["current_phase"] = "HEROES_CLEARING_PHASE"
            game_state["boss_phase"] = f"⚔️ HERÓIS RESOLVENDO {target_clear} CARDS!"

            wave_timer = 180
            while game_state["cards_cleared_in_current_wave"] < target_clear and wave_timer > 0:
                if game_state.get("boss_hp", 100) <= 0: break
                wave_timer -= 1
                game_state["phase_timer_sec"] = wave_timer
                duel = game_state["duel"]

                if not duel["is_active"] and game_state["kanban"]["to_do"]:
                    card = game_state["kanban"]["to_do"].pop(0)
                    card["status"] = "EM PROGRESSO"
                    game_state["kanban"]["in_progress"].append(card)

                    hero_key = await felipe_analyze_and_delegate_card_async(card)
                    hero = pixel_agents[hero_key]
                    card["branch_name"] = f"feature/{card['id'].lower()}-{hero_key}"

                    if str(card["id"]).startswith(f"{settings.jira_project_key}-"):
                        _, tr_code = await asyncio.to_thread(jira_client.transition_issue, card["id"], "Fazendo")
                        if tr_code == 404: purge_card_from_kanban(card["id"]); continue
                    
                    pixel_agents["felipe"]["action"] = f"🧠 Roteou [{card['id']}]"
                    
                    # INÍCIO DO DUELO - TIMEOUT ALTO E KILL FLAG ZERADO
                    game_state["duel"] = {
                        "is_active": True, "active_hero": hero["name"], "hero_key": hero_key,
                        "active_card": card, "timeout_timer_sec": 150.0,
                        "max_timeout_sec": 150.0, "phase": "hero_coding", "last_code": "# Inicializando ambiente e poderes...\n\n",
                        "llm_finished": False, "commit_info": None, "active_power": "⚡ PREPARANDO",
                        "kill_flag": False
                    }
                    duel = game_state["duel"]

                    async def background_llm_worker(c_id, b_name):
                        def chunk_handler(chunk):
                            if game_state["duel"]["is_active"] and game_state["duel"]["active_card"]["id"] == c_id:
                                game_state["duel"]["last_code"] += chunk
                        
                        def check_cancel():
                            return game_state["duel"].get("kill_flag", False)

                        commit_res = await synthesize_code_and_commit_stream(
                            hero["name"], hero["class"], card["title"], card.get("description", ""),
                            str(card["id"]), b_name, hero["learned_skills"], chunk_handler, check_cancel
                        )
                        
                        if game_state["duel"]["is_active"] and game_state["duel"]["active_card"]["id"] == c_id and not check_cancel():
                            game_state["duel"]["commit_info"] = commit_res
                            game_state["duel"]["llm_finished"] = True

                    asyncio.create_task(background_llm_worker(card["id"], card["branch_name"]))

                if not duel["is_active"]:
                    await asyncio.sleep(1.0); continue

                hero_key = duel["hero_key"]
                hero = pixel_agents[hero_key]
                c_duel = duel["active_card"]

                if duel["phase"] == "hero_coding":
                    if duel.get("llm_finished"):
                        c_duel["commit_info"] = duel["commit_info"]
                        c_duel["status"] = "EM VALIDAÇÃO"
                        if c_duel in game_state["kanban"]["in_progress"]: game_state["kanban"]["in_progress"].remove(c_duel)
                        game_state["kanban"]["in_validation"].append(c_duel)

                        if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"):
                            await asyncio.to_thread(jira_client.transition_issue, str(c_duel["id"]), "Em análise")
                            safe_jira_comment(c_duel["id"], hero["name"], f"🤖 **PR Aberto:** Branch `{c_duel['branch_name']}`.")

                        game_state["boss_phase"] = f"🔍 PO AUDITANDO PR `{c_duel['branch_name']}`!"
                        duel["phase"] = "in_validation"
                        duel["timeout_timer_sec"] = 6.0
                    else:
                        duel["timeout_timer_sec"] -= 1.0
                        timeout_pct = max(0.0, duel["timeout_timer_sec"] / duel["max_timeout_sec"])
                        
                        p_name = random.choice(hero["learned_skills"]) if hero.get("learned_skills") else "FAST CODING"
                        if timeout_pct < 0.25: duel["active_power"] = f"🌟 {p_name.upper()} (OVERDRIVE)"
                        elif timeout_pct < 0.50: duel["active_power"] = f"🔮 {p_name} (FOCUS)"
                        else: duel["active_power"] = f"⚡ {p_name}"

                        if duel["timeout_timer_sec"] <= 0:
                            # ====================================================
                            # 💀 MORTE SÚBITA - ZERANDO O HERÓI E MATANDO PROCESSO
                            # ====================================================
                            duel["kill_flag"] = True # Mata a leitura do HTTP de imediato
                            
                            c_duel["rejections"] += 1; c_duel["status"] = "A FAZER"
                            if c_duel in game_state["kanban"]["in_progress"]: game_state["kanban"]["in_progress"].remove(c_duel)
                            game_state["kanban"]["to_do"].append(c_duel)
                            
                            if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"):
                                await asyncio.to_thread(jira_client.transition_issue, c_duel["id"], "A fazer")
                                safe_jira_comment(c_duel["id"], "System", f"💀 **KILLED!** O tempo limite ({duel['max_timeout_sec']}s) esgotou.\n\n🔻 **Punição Brutal:** {hero['name']} sofreu burnout! Perdeu todo o XP e foi resetado pro Nível 1.")

                            # Reseta o Herói sem dó!
                            hero["skill_level"] = 1
                            hero["xp"] = 0
                            if hero.get("learned_skills"):
                                hero["learned_skills"] = [hero["learned_skills"][0]] # Volta só com a primeira skill

                            game_state["boss_phase"] = f"💀 {hero['name'].upper()} KILLED! RESET LVL 1!"
                            audit_logs.append({"event_id": f"evt_{len(audit_logs)+1}", "action": f"KILLED & RESET: {hero['name']}", "card_id": c_duel["id"]})

                            duel["is_active"] = False; duel["phase"] = "idle"

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
                                if c_duel in game_state["kanban"]["in_validation"]: game_state["kanban"]["in_validation"].remove(c_duel)
                                game_state["kanban"]["done"].append(c_duel)
                                game_state["cards_cleared_in_current_wave"] += 1
                                game_state["total_real_commits"] += 1

                                linhas = commit_info.get("lines_added", 5)
                                hero["xp"] += (linhas * 10)
                                novo_poder = await asyncio.to_thread(local_llm_client.extract_skill_from_card, c_duel["title"], c_duel.get("description", ""))
                                if novo_poder not in hero["learned_skills"]: hero["learned_skills"].append(novo_poder)

                                if hero["xp"] >= (hero["skill_level"] * 100):
                                    hero["skill_level"] += 1; hero["xp"] = 0

                                if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"):
                                    await asyncio.to_thread(jira_client.transition_issue, c_duel["id"], "Feito")
                                    safe_jira_comment(c_duel["id"], "PO Auditor", f"✅ **MERGE APROVADO!**\nNovo Poder: {novo_poder}")

                                damage = 150 + (hero["skill_level"] * 30) + (linhas * 2)
                                game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                                game_state["boss_phase"] = f"✅ MERGE! -{damage}HP | Poder Ganho: {novo_poder}!"
                                audit_logs.append({"event_id": f"evt_{len(audit_logs)+1}", "action": f"Skill Acquired: {novo_poder}", "card_id": c_duel["id"]})
                            else: approved = False
                        
                        if not approved:
                            c_duel["rejections"] += 1; c_duel["status"] = "A FAZER"
                            if c_duel in game_state["kanban"]["in_validation"]: game_state["kanban"]["in_validation"].remove(c_duel)
                            game_state["kanban"]["to_do"].append(c_duel)
                            if str(c_duel["id"]).startswith(f"{settings.jira_project_key}-"): await asyncio.to_thread(jira_client.transition_issue, c_duel["id"], "A fazer")

                        duel["is_active"] = False; duel["phase"] = "idle"

                await asyncio.sleep(1.0)
            await asyncio.sleep(2)
        except Exception as outer_e:
            logger.error(f"[Main Loop Exception] {outer_e}")
            await asyncio.sleep(2.0)

async def background_compliance_auditor_worker():
    await asyncio.sleep(10)
    while True:
        try:
            check_list = [(c, col) for col in ["in_progress", "in_validation", "done"] for c in list(game_state["kanban"].get(col, []))]
            for card, col in check_list:
                card_id = str(card.get("id", ""))
                if not card_id.startswith(f"{settings.jira_project_key}-"): continue
                try:
                    details, http_code = await asyncio.to_thread(jira_client.get_issue_details, card_id)
                    if http_code == 404: purge_card_from_kanban(card_id); continue
                except Exception: pass
                await asyncio.sleep(0.5)
        except Exception: pass
        await asyncio.sleep(25)


# ====================================================================
# FASTAPI SERVER E DASHBOARD WEB
# ====================================================================

app = FastAPI(title="FLOSE AEOS — Dynamic Self-Learning Multi-Agent")

@app.on_event("startup")
async def startup_event():
    loaded_gs, loaded_pa, loaded_al = load_persisted_state()
    if loaded_gs and loaded_pa: game_state.update(loaded_gs); pixel_agents.update(loaded_pa)

    if _config_problems: game_state["jira_project_valid"] = False
    else:
        project_key = settings.jira_project_key
        if not await asyncio.to_thread(jira_client.verify_project_access, project_key): game_state["jira_project_valid"] = False
        else:
            game_state["jira_project_valid"] = True
            try:
                live_cards = await asyncio.to_thread(jira_client.fetch_real_jira_issues, project_key, 100)
                new_kanban = {"to_do": [], "in_progress": [], "in_validation": [], "done": []}
                local_data = {c["id"]: c for col in game_state["kanban"].values() for c in col}
                
                for jc in live_cards:
                    card = local_data.get(jc["id"], jc)
                    card.update({"title": jc["title"], "status": jc["status"], "parent": jc["parent"]})
                    if card["status"] == "A FAZER": new_kanban["to_do"].append(card)
                    elif card["status"] == "EM PROGRESSO": new_kanban["in_progress"].append(card)
                    elif card["status"] == "EM VALIDAÇÃO": new_kanban["in_validation"].append(card)
                    elif card["status"] == "CONCLUÍDO": new_kanban["done"].append(card)

                game_state["kanban"] = new_kanban
            except Exception: pass

    asyncio.create_task(save_state_to_disk())
    asyncio.create_task(main_engine_loop())
    asyncio.create_task(background_compliance_auditor_worker())

@app.get("/api/boss/state")
async def get_state():
    for agent in pixel_agents.values():
        agent["x"] = max(50, min(550, agent["x"] + random.choice([-2, 0, 2])))
        agent["y"] = max(200, min(320, agent["y"] + random.choice([-2, 0, 2])))
    return {"game_state": game_state, "pixel_agents": list(pixel_agents.values()), "duel": game_state["duel"], "kanban": game_state["kanban"], "audit_logs": audit_logs[-10:]}

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>FLOSE AEOS — Dynamic Self-Learning</title>
        <link href="[https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap](https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap)" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { background: #0d0e15; color: #fff; font-family: 'Press Start 2P', monospace; overflow: hidden; }
            #game-container { display: flex; width: 100vw; height: 100vh; }
            #pixel-canvas { background: #181926; border-right: 4px solid #3b3d54; image-rendering: pixelated; flex-shrink: 0; }
            .side-panel { flex: 1; background: #11121d; padding: 1rem; display: flex; flex-direction: column; gap: 0.6rem; border-left: 4px solid #3b3d54; overflow-y: auto; }
            .hud-title { font-size: 0.6rem; color: #55ff55; text-shadow: 2px 2px #00aa00; text-align: center; padding: 0.4rem; border-bottom: 2px solid #1f2040; }
            .turn-banner { background: rgba(168, 85, 247, 0.15); border: 2px solid #a855f7; border-radius: 6px; padding: 0.5rem 0.8rem; text-align: center; font-size: 0.48rem; line-height: 1.6; }
            .duel-arena-box { background: rgba(59, 130, 246, 0.1); border: 2px solid #3b82f6; border-radius: 8px; padding: 0.7rem; min-height: 220px;}
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
            .kanban-card-item { background: rgba(255,255,255,0.05); border: 1px solid #30363d; border-radius: 4px; padding: 0.35rem; margin-bottom: 0.35rem; font-size: 0.34rem; line-height: 1.4; }
            .kanban-card-item.active-card { border-color: #60a5fa; background: rgba(59, 130, 246, 0.12); animation: pulse-card 1s ease-in-out infinite alternate; }
            .kanban-card-item.rejected-card { border-color: #ff5555; background: rgba(255, 85, 85, 0.08); }
            @keyframes pulse-card { from { box-shadow: 0 0 4px rgba(59,130,246,0.3); } to { box-shadow: 0 0 10px rgba(59,130,246,0.8); } }
            .audit-log-entry { font-size: 0.36rem; color: #9ca3af; margin-bottom: 0.2rem; line-height: 1.4; }
            .code-terminal { background: #050505; border: 1px solid #1f2937; border-radius: 4px; padding: 0.5rem; margin-top: 0.5rem; color: #10b981; font-family: 'Courier New', Courier, monospace; font-size: 0.35rem; white-space: pre-wrap; overflow-y: auto; max-height: 180px; box-shadow: inset 0 0 10px rgba(0,0,0,0.8); text-align: left; }
            .cursor { animation: blink 1s step-end infinite; }
            @keyframes blink { 50% { opacity: 0; } }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>
            <div class="side-panel">
                <div class="hud-title">⚡ FLOSE AEOS — LEARNING ENGINE</div>
                <div id="turn-banner" class="turn-banner">FASE ATUAL: CARREGANDO...</div>
                <div id="duel-box" class="duel-arena-box">
                    <div style="font-size:0.46rem; color:#60a5fa; text-align:center;">AGUARDANDO PROCESSO...</div>
                </div>
                <div class="kanban-grid">
                    <div class="kanban-col"><div class="kanban-col-title card-todo" id="title-todo">🔴 A FAZER (0)</div><div class="kanban-col-cards" id="col-todo"></div></div>
                    <div class="kanban-col"><div class="kanban-col-title card-progress" id="title-progress">🔵 EM PROGRESSO (0)</div><div class="kanban-col-cards" id="col-progress"></div></div>
                    <div class="kanban-col"><div class="kanban-col-title card-validation" id="title-validation">🟡 EM VALIDAÇÃO (0)</div><div class="kanban-col-cards" id="col-validation"></div></div>
                    <div class="kanban-col"><div class="kanban-col-title card-done" id="title-done">🟢 CONCLUÍDO (0)</div><div class="kanban-col-cards" id="col-done"></div></div>
                </div>
                <div>
                    <div style="font-size:0.44rem; color:#a855f7; margin-bottom:0.3rem;">
                        🐙 COMMITS REAIS <span id="commit-count" style="color:#22c55e; font-size:0.38rem;"></span>
                    </div>
                </div>
                <div>
                    <div style="font-size:0.42rem; color:#55ff55; margin-bottom:0.2rem;">📜 AUDIT LOG & SKILLS</div>
                    <div id="audit-log" style="max-height: 80px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('pixel-canvas');
            const ctx = canvas.getContext('2d');
            function resizeCanvas() { canvas.width = Math.floor(window.innerWidth * 0.52); canvas.height = window.innerHeight; }
            resizeCanvas(); window.addEventListener('resize', resizeCanvas);

            let gameState = {}; let agentsList = []; let duelState = {}; let kanbanState = {};

            function drawPixelSprite(x, y, color, name, isDuelist, lvl, action) {
                const blink = Math.floor(Date.now() / 500) % 2 === 0;
                ctx.fillStyle = color; ctx.fillRect(x, y + 10, 24, 20);
                ctx.fillStyle = "#ffcc99"; ctx.fillRect(x + 4, y, 16, 14);
                ctx.fillStyle = "#000"; ctx.fillRect(x + 7, y + 4, 3, 3); ctx.fillRect(x + 14, y + 4, 3, 3);
                ctx.font = '7px "Press Start 2P"'; ctx.fillStyle = color; ctx.fillText(`${name} Lv.${lvl}`, x - 8, y - 12);
                if (action) { ctx.font = '5px "Press Start 2P"'; ctx.fillStyle = "#9ca3af"; ctx.fillText(action.substring(0, 32), x - 20, y - 3); }
                if (isDuelist) {
                    if (blink) { ctx.strokeStyle = "#60a5fa"; ctx.lineWidth = 2; ctx.strokeRect(x - 3, y - 3, 30, 36); }
                    ctx.fillStyle = "#3b82f6"; ctx.fillRect(x - 2, y - 24, 28, 9);
                    ctx.font = '5px "Press Start 2P"'; ctx.fillStyle = "#fff"; ctx.fillText("⚔️ DUELO", x, y - 17);
                }
            }

            function drawPOBoss(hpPercent, phaseText) {
                const bx = canvas.width / 2 - 40; const by = 55; const bossAnim = Math.sin(Date.now() / 400) * 3;
                ctx.fillStyle = "#1e1e2e"; ctx.fillRect(bx, by + 30 + bossAnim, 80, 70);
                ctx.fillStyle = "#ff0000"; ctx.fillRect(bx + 36, by + 35 + bossAnim, 8, 35);
                ctx.fillStyle = "#313244"; ctx.fillRect(bx + 10, by + bossAnim, 60, 40);
                ctx.fillStyle = "#ff0000"; ctx.fillRect(bx + 18, by + 12 + bossAnim, 14, 10); ctx.fillRect(bx + 48, by + 12 + bossAnim, 14, 10);
                ctx.fillRect(bx + 15, by - 10 + bossAnim, 8, 14); ctx.fillRect(bx + 57, by - 10 + bossAnim, 8, 14);
                ctx.font = '9px "Press Start 2P"'; ctx.fillStyle = "#ff5555"; ctx.fillText("👹 PO EVIL BOSS", bx - 30, by - 20 + bossAnim);

                const hpBarW = 320; const hpBarX = canvas.width / 2 - hpBarW / 2;
                ctx.fillStyle = "#440000"; ctx.fillRect(hpBarX, 12, hpBarW, 18);
                const hpColor = hpPercent > 60 ? "#ff3333" : hpPercent > 30 ? "#ff8800" : "#ff0000";
                ctx.fillStyle = hpColor; ctx.fillRect(hpBarX, 12, (hpBarW * Math.max(0, hpPercent)) / 100, 18);
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.strokeRect(hpBarX, 12, hpBarW, 18);
                ctx.font = '6px "Press Start 2P"'; ctx.fillStyle = "#ffffff"; ctx.fillText(`HP: ${Math.round(Math.max(0, hpPercent))}%`, hpBarX + 4, 25);
                ctx.font = '5px "Press Start 2P"'; ctx.fillStyle = "#ffaa00"; ctx.fillText(phaseText ? phaseText.substring(0, 65) : "", canvas.width / 2 - 160, by + 120 + bossAnim);
            }

            function render() {
                ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = "#11111b"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < canvas.width; i += 40) { ctx.strokeStyle = "#1a1b2e"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke(); }
                for (let j = 0; j < canvas.height; j += 40) { ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(canvas.width, j); ctx.stroke(); }

                if (gameState && gameState.boss_max_hp) {
                    const hpPct = (gameState.boss_hp / gameState.boss_max_hp) * 100; drawPOBoss(hpPct, gameState.boss_phase || "");
                    agentsList.forEach(a => {
                        const isDuelist = duelState && duelState.is_active && duelState.active_hero === a.name;
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, isDuelist, a.skill_level, a.action);
                    });
                    ctx.font = '8px "Press Start 2P"'; ctx.fillStyle = "#55ff55"; ctx.fillText(`⏱️ ${gameState.phase_timer_sec || 0}s`, canvas.width / 2 - 30, canvas.height - 20);
                }
                requestAnimationFrame(render);
            }
            render();

            async function updateState() {
                try {
                    const res = await fetch('/api/boss/state'); const data = await res.json();
                    gameState = data.game_state; agentsList = data.pixel_agents; duelState = data.duel; kanbanState = data.kanban; const auditLogs = data.audit_logs;

                    const banner = document.getElementById('turn-banner');
                    banner.innerHTML = `⚙️ ENGINE | COMMITS: ${gameState.cards_processed_count || 0}`;
                    
                    const duel = duelState;
                    if (duel && duel.is_active && duel.active_card) {
                        let pct = 0;
                        if(duel.phase === 'hero_coding') pct = Math.max(0, (duel.timeout_timer_sec / duel.max_timeout_sec) * 100);
                        else if(duel.phase === 'in_validation') pct = Math.max(0, (duel.timeout_timer_sec / 6.0) * 100);

                        const timerColor = pct > 50 ? '#00ff00' : pct > 25 ? '#ffaa00' : '#ff5555';
                        
                        let phaseLabel = '';
                        let phaseColor = '';
                        if (duel.phase === 'hero_coding') {
                            phaseLabel = '🧠 IA CODIFICANDO AO VIVO...';
                            phaseColor = '#a855f7';
                        } else {
                            phaseLabel = '🔍 PO AUDITANDO CÓDIGO';
                            phaseColor = '#ffaa00';
                        }
                        
                        let htmlContent = `
                            <div style="font-size:0.52rem; color:${phaseColor}; font-weight:bold; margin-bottom:0.25rem; text-align:center;">${phaseLabel}</div>
                            <div style="font-size:0.46rem; color:#fff; margin-bottom:0.2rem;">⚔️ <b>Herói:</b> <span style="color:#a855f7;">${duel.active_hero}</span></div>
                            <div style="font-size:0.42rem; color:#55ff55; font-weight:bold; margin-bottom:0.15rem;">USANDO PODER: ${duel.active_power || '...'}</div>
                            <div style="font-size:0.38rem; color:${timerColor}; font-weight:bold; margin-bottom:0.25rem;">⏱️ TEMPO RESTANTE: ${Math.max(0, duel.timeout_timer_sec).toFixed(1)}s</div>
                        `;

                        if ((duel.phase === 'hero_coding' || duel.phase === 'in_validation') && typeof duel.last_code === 'string') {
                            const escapedCode = duel.last_code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                            htmlContent += `<div class="code-terminal" id="term-box">${escapedCode}<span class="cursor">_</span></div>`;
                        }
                        
                        htmlContent += `<div class="duel-timer-bg"><div class="duel-timer-fill" style="width:${pct}%; background:${timerColor};"></div></div>`;
                        document.getElementById('duel-box').innerHTML = htmlContent;

                        setTimeout(() => {
                            const term = document.getElementById('term-box');
                            if(term) term.scrollTop = term.scrollHeight;
                        }, 10);

                    } else {
                        document.getElementById('duel-box').innerHTML = `<div style="font-size:0.46rem; color:#9ca3af; text-align:center; padding:0.5rem;">😴 AGUARDANDO CARD...</div>`;
                    }

                    const activeCardId = duel && duel.active_card ? duel.active_card.id : null;
                    const todoCards = kanbanState.to_do || []; const progressCards = kanbanState.in_progress || [];
                    const validationCards = kanbanState.in_validation || []; const doneCards = kanbanState.done || [];

                    document.getElementById('title-todo').textContent = `🔴 A FAZER (${todoCards.length})`; document.getElementById('title-progress').textContent = `🔵 PROGRESSO (${progressCards.length})`;
                    document.getElementById('title-validation').textContent = `🟡 REVISÃO (${validationCards.length})`; document.getElementById('title-done').textContent = `🟢 FEITO (${doneCards.length})`;

                    function renderCards(cards, colorClass) {
                        if (!cards || cards.length === 0) return '';
                        return cards.map(c => `
                            <div class="kanban-card-item ${c.id === activeCardId ? 'active-card' : ''}">
                                <a href="[https://felipeflose.atlassian.net/browse/$](https://felipeflose.atlassian.net/browse/$){c.id}" target="_blank" style="color:${colorClass};">${c.id}</a>
                                <div style="font-size:0.34rem; color:#e5e7eb; margin-top:0.2rem;">${c.title}</div>
                            </div>
                        `).join('');
                    }
                    document.getElementById('col-todo').innerHTML = renderCards(todoCards, '#ff5555'); document.getElementById('col-progress').innerHTML = renderCards(progressCards, '#60a5fa');
                    document.getElementById('col-validation').innerHTML = renderCards(validationCards, '#ffaa00'); document.getElementById('col-done').innerHTML = renderCards(doneCards, '#55ff55');
                    document.getElementById('commit-count').textContent = `(${gameState.total_real_commits || 0} commits ✅)`;
                    document.getElementById('audit-log').innerHTML = auditLogs.map(l => `<div class="audit-log-entry">» [${l.action}] ${(l.reason || l.card_id || '').substring(0, 55)}</div>`).join('');
                } catch(e) {}
            }
            updateState(); setInterval(updateState, 400);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.port)