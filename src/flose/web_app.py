import asyncio
import time
import random
import os
import subprocess
import json
import inspect
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Tuple

from flose.bus.event_bus import EventBus
from flose.core.models import (
    AgentIdentity,
    AgentTier,
    TaskSpecification,
    TaskStatus,
    PriorityLevel,
    SecurityContext,
    FLOSEMessage,
)
from flose.engines.planning import PlanningEngine
from flose.engines.governance import GovernanceEngine
from flose.connectors.jira import JiraConnector
from flose.connectors.gemma_local import GemmaLocalConnector
from flose.engines.code_synthesis import synthesize_and_commit_real_code
from flose.core.persistence import load_persisted_state, save_state_to_disk
from flose.agents.po_auditor import scan_host_codebase

app = FastAPI(title="FLOSE AEOS - Real GitHub Skill Commit Engine")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

REPO_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILLS_DOC_PATH = os.path.join(REPO_PATH, "docs", "skills_learned.md")

# Busca os cards REAIS do Jira Cloud
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=1000)
for c in real_jira_cards:
    c.setdefault("rejections", 0)

# 💾 RESTAURA ESTADO PERSISTIDO DO DISCO
loaded_gs, loaded_pa, loaded_al = load_persisted_state()

if loaded_gs and loaded_pa:
    game_state = loaded_gs
    pixel_agents = loaded_pa
    audit_logs = loaded_al if loaded_al else []
    
    existing_ids = set()
    for col in game_state["kanban"].values():
        for card_item in col:
            existing_ids.add(card_item.get("id"))
            
    for c in real_jira_cards:
        if c.get("id") not in existing_ids:
            game_state["kanban"]["to_do"].append(c)

    valid_done = []
    for c in game_state["kanban"]["done"]:
        if c.get("commit_info") and c.get("delegated_to"):
            valid_done.append(c)
        else:
            c["status"] = "A FAZER"
            game_state["kanban"]["to_do"].append(c)
    game_state["kanban"]["done"] = valid_done

    print(f"[Persistence] Restaurado! Boss HP: {game_state['boss_hp']}/{game_state['boss_max_hp']} | Cards Done Válidos: {len(game_state['kanban']['done'])}")
else:
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
            "git_branch": None,
            "timeout_timer_sec": 18.0,
            "max_timeout_sec": 18.0,
            "damage_dealt": 0,
            "work_progress": 0.0,
            "phase": "idle"  # idle | picking | announcing | creating_branch | coding | submitting_commit | in_validation
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
    """Salva o estado do jogo periodicamente no disco."""
    while True:
        await asyncio.sleep(2.0)
        await save_state_to_disk(game_state, pixel_agents, audit_logs)

# ============================================================
# HELPER DE JIRA COMMENT & GIT INSPECTION
# ============================================================
async def safe_jira_comment(card_id: str, comment_text: str, author_name: str = "FLOSE Agent"):
    """Envia um comentário assíncrono para o card no Jira Cloud se for um ID KAN-."""
    if str(card_id).startswith("KAN-"):
        try:
            await asyncio.to_thread(jira.add_comment, card_id, comment_text, author_name)
        except Exception as e:
            print(f"[Jira Comment Error] Falha ao comentar em {card_id}: {e}")

async def create_git_feature_branch(card_id: str, hero_name: str) -> str:
    """Cria uma branch local/remota de feature para o card e faz checkout."""
    clean_id = str(card_id).lower().replace(" ", "-")
    clean_hero = str(hero_name).lower()
    branch_name = f"feature/{clean_id}-{clean_hero}"
    
    try:
        await asyncio.to_thread(
            subprocess.run,
            ["git", "checkout", "-b", branch_name],
            cwd=REPO_PATH, capture_output=True, text=True
        )
    except Exception as e:
        print(f"[Git Branch Local Error] {e}")

    return branch_name

async def verify_git_commit_exists_in_repo(commit_hash: str) -> bool:
    """Verifica se o commit REALMENTE existe no banco do Git local."""
    if not commit_hash or commit_hash == "????":
        return False
    try:
        res = await asyncio.to_thread(
            subprocess.run,
            ["git", "cat-file", "-t", commit_hash],
            cwd=REPO_PATH, capture_output=True, text=True
        )
        return res.returncode == 0 and "commit" in res.stdout.strip()
    except Exception:
        return False

# ============================================================
# REAL GITHUB COMMIT ENGINE
# ============================================================
_git_commit_lock = asyncio.Lock()

async def push_real_github_skill_commit(agent_name: str, skill_name: str) -> str:
    """Faz um commit REAL no GitHub com a nova skill aprendida."""
    async with _git_commit_lock:
        try:
            os.makedirs(os.path.dirname(SKILLS_DOC_PATH), exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"- [{timestamp}] [{agent_name}] aprendeu: **{skill_name}**\n"
            
            with open(SKILLS_DOC_PATH, "a", encoding="utf-8") as f:
                f.write(entry)

            commit_msg = f"feat(skills-{agent_name.lower()}): {agent_name} learned '{skill_name}' - auto commit by FLOSE AEOS"

            await asyncio.to_thread(
                subprocess.run,
                ["git", "add", "docs/skills_learned.md"],
                cwd=REPO_PATH, capture_output=True, text=True
            )

            result_commit = await asyncio.to_thread(
                subprocess.run,
                ["git", "commit", "-m", commit_msg],
                cwd=REPO_PATH, capture_output=True, text=True
            )

            if result_commit.returncode != 0:
                return f"[skip] {skill_name} (nada novo para commitar)"

            await asyncio.to_thread(
                subprocess.run,
                ["git", "push", "origin", "main"],
                cwd=REPO_PATH, capture_output=True, text=True
            )

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
# JIRA CARD CREATION
# ============================================================
async def create_real_jira_card_async():
    try:
        smell_report = await asyncio.to_thread(scan_host_codebase, "src/flose")
        if smell_report:
            title, desc = smell_report
        else:
            title = f"Refatorar Componente X{random.randint(10,99)}"
            desc = "Não foram achadas falhas estruturais pelo AST. Faça uma revisão geral de segurança."
            
        await async_create_jira_card_background(title, desc)
    except Exception as e:
        print(f"[Create Real Card Error] {e}")

async def async_create_jira_card_background(topic_title: str, topic_desc: str):
    try:
        jira_res = await asyncio.to_thread(
            jira.create_detailed_epic_or_task, "KAN", topic_title, topic_desc, "ÉPICO PO FRENZY"
        )
        new_key = jira_res.get("key", f"KAN-{random.randint(9700, 9999)}")
        new_card = {
            "id": new_key,
            "title": f"[PO-FRENZY] {topic_title}",
            "description": topic_desc,
            "status": "A FAZER",
            "rejections": 0,
            "po_rejection_reason": "",
            "comments": [{"author": "PO EVIL BOSS", "text": f"Criado na rajada de 30s: {topic_title}."}]
        }
        game_state["kanban"]["to_do"].append(new_card)
        game_state["boss_cards_created_in_frenzy"] += 1
        audit_logs.append({
            "event_id": f"evt_{len(audit_logs)+1}",
            "action": "PO_FRENZY_CARD_CREATED_JIRA",
            "card_id": new_key,
            "title": topic_title[:40]
        })
    except Exception as e:
        print(f"[Async Jira Error] {e}")

# ============================================================
# VILÃO VALIDA O COMMIT NO GIT REAL
# ============================================================
async def po_vilao_inspect_commit_code_async(card: Dict[str, Any], commit_info: Dict[str, Any]) -> Tuple[bool, str]:
    """
    O PO Vilão inspeciona o COMMIT REAL no Git + O PROCESSO INTERNO DE ENGENHARIA!
    Valida existência no Git, Pytest, qualidade de código e conformidade de processo.
    """
    if not commit_info or not commit_info.get("success"):
        return False, "❌ PROCESSO/GIT AUDIT: Commit não foi registrado com sucesso no Git!"

    commit_hash = commit_info.get("commit_hash", "????")
    file_path = commit_info.get("file_path", "")
    lines_added = commit_info.get("lines_added", 0)
    test_passed = commit_info.get("test_passed", False)
    commit_msg = commit_info.get("commit_msg", "")

    # ============================================================
    # 🔍 ETAPA 1: AUDITORIA DE PROCESSO INTERNO E GOVERNANÇA (NEW!)
    # ============================================================
    
    # 1.1 Validar padrão de mensagem de commit (Conventional Commits)
    msg_to_check = commit_msg.lower().strip()
    if msg_to_check.startswith("commit "):
        parts = msg_to_check.split(":", 1)
        if len(parts) > 1:
            msg_to_check = parts[1].strip()

    valid_prefixes = ["feat(", "fix(", "refactor(", "docs(", "test(", "chore("]
    if not any(msg_to_check.startswith(p) for p in valid_prefixes):
        return False, f"❌ PROCESSO AUDIT ({commit_hash}): Mensagem de commit '{commit_msg[:40]}' fora do padrão Conventional Commits! Ex: feat(modulo): resumo"

    # 1.2 Validar se o plano de ação definido pelo Felipe foi registrado
    if not card.get("action_plan"):
        return False, f"❌ PROCESSO AUDIT ({card.get('id')}): Faltou o plano de ação de arquitetura registrado no card!"

    # ============================================================
    # 🐙 ETAPA 2: AUDITORIA TÉCNICA DE GIT & CÓDIGO
    # ============================================================

    # 2.1 Auditoria Física do Hash no Repositório Git
    commit_exists = await verify_git_commit_exists_in_repo(commit_hash)
    if not commit_exists:
        return False, f"❌ GIT AUDIT: O commit '{commit_hash}' NÃO existe no repositório Git real!"

    # 2.2 Auditoria Pytest
    if not test_passed:
        return False, f"❌ CODE AUDIT ({commit_hash}): O arquivo {file_path} FALHOU na suíte de testes do Pytest!"

    # 2.3 Auditoria de Volume de Código
    if lines_added < 15:
        return False, f"❌ CODE AUDIT ({commit_hash}): O arquivo {file_path} tem apenas {lines_added} linhas! Código insuficiente para o padrão da squad!"

    # 2.4 Leitura do Arquivo Físico no Disco e Verificação de Palavras-Chave
    abs_file_path = os.path.join(REPO_PATH, file_path) if file_path else ""
    if not abs_file_path or not os.path.exists(abs_file_path):
        return False, f"❌ GIT AUDIT ({commit_hash}): Módulo {file_path} não foi encontrado no disco!"

    try:
        with open(abs_file_path, "r", encoding="utf-8") as f:
            code_text = f.read().lower()

        card_title = (card.get("title") or "").lower()
        
        required_keywords = []
        if any(k in card_title for k in ["xss", "sql", "secur", "sanitiz"]):
            required_keywords = ["sanitize", "sql"]
        elif any(k in card_title for k in ["async", "performance", "backend", "cache"]):
            required_keywords = ["async", "cache"]
        elif any(k in card_title for k in ["ui", "pixel", "frontend", "grid"]):
            required_keywords = ["grid", "hsl"]

        missing = [kw for kw in required_keywords if kw not in code_text]
        if missing:
            return False, f"❌ REQUISITO AUDIT ({commit_hash}): O código em {file_path} não atendeu os critérios do card. Faltou: {', '.join(missing)}!"
            
    except Exception as e:
        return False, f"❌ AUDIT ERROR: Erro crítico ao inspecionar artefatos: {e}"

    # Escudo ativo garante aprovação
    if card.get("shield_active"):
        return True, f"✅ AUDIT COMPLETE ({commit_hash}): Protegido por Escudo QA! Código e Processo aprovados na íntegra!"

    # Risco de cobrança de melhoria de processo adicional pelo PO Vilão (20% de chance)
    if random.random() < 0.20 and card.get("rejections", 0) < 2:
        po_process_critiques = [
            "PO exigiu adicionar docstrings no padrão Google nas funções antes de subir p/ main!",
            "PO exigiu adicionar typing explícito em todos os retornos do módulo!",
            "PO exigiu criar um cenário de teste de borda adicional para falhas de rede/timeout!"
        ]
        chosen_critique = random.choice(po_process_critiques)
        return False, f"❌ PROCESSO IMPROVEMENT ({commit_hash}): {chosen_critique}"

    return True, f"✅ ALL AUDITS APPROVED ({commit_hash}): Código, Pytest e Processo de Engenharia validados! Pronto para Merge na Main!"
# ============================================================
# DELEGATION & TIMEOUT POWERS
# ============================================================
def felipe_analyze_and_delegate_card(card: Dict[str, Any]) -> Tuple[str, str, str]:
    """
    Felipe (Líder de Arquitetura) analisa o card específico do Jira e gera
    um plano de ação ÚNICO e contextualizado com base no título e descrição da tarefa.
    Retorna: (assigned_hero_key, delegation_reason, action_plan)
    """
    card_id = card.get("id", "KAN-X")
    title = card.get("title", "Refatoração").strip()
    desc = card.get("description", "Sem descrição detalhada.").strip()
    full_text = f"{title} {desc}".lower()

    # 1. Roteamento inteligente de especialista
    if any(k in full_text for k in ["gemma", "ollama", "prompt", "ia", "analys", "fine-tuning", "modelo"]):
        assigned = "sofia"
        domain = "Inteligência Artificial & LLMs"
    elif any(k in full_text for k in ["refator", "async", "perform", "rust", "backend", "cache", "speed"]):
        assigned = "lucas"
        domain = "Sistemas Assíncronos e Alta Performance"
    else:
        assigned = "beatriz"
        domain = "Segurança, Sanitização e Testes de Aceite"

    hero_name = pixel_agents[assigned]["name"]

    # 2. Extração de palavras-chave para personalização dinâmica do escopo
    target_component = "módulo principal"
    if "componente" in full_text:
        words = title.split()
        target_component = words[-1] if words else "componente alvo"
    elif "xss" in full_text or "sql" in full_text:
        target_component = "camada de entrada/sanitização de dados"
    elif "async" in full_text or "cache" in full_text:
        target_component = "pipeline de execução backend"

    # 3. Construção do motivo e plano de ação dinâmico ÚNICO para ESTE card
    reason = f"Análise de Arquitetura: Card [{card_id}] exige intervenção especialista em {domain}."

    action_plan = (
        f"1. **Mapeamento:** Inspecionar o impacto direto de '{title}' no repositório.\n"
        f"2. **Implementação:** Desenvolver a solução focando em {target_component}, seguindo os padrões do FLOSE.\n"
        f"3. **Validação:** Criar testes específicos no Pytest para garantir que o cenário '{title[:35]}...' passe sem regressão."
    )

    # 4. Atualiza o card com o contexto enriquecido
    card["delegated_by"] = "Felipe (Líder de Arquitetura)"
    card["delegated_to"] = hero_name
    card["delegation_note"] = reason
    card["action_plan"] = action_plan

    return assigned, reason, action_plan
def trigger_hero_timeout_power(hero_key: str, timeout_pct: float) -> Tuple[float, float, str, int, bool]:
    hero = pixel_agents[hero_key]

    if timeout_pct < 0.25:
        power_id = random.randint(10000, 13000)
        if hero_key == "sofia":
            power_name = f"🌟 GEMMA 4 QUANTUM BEAM (Power #{power_id})"
        elif hero_key == "lucas":
            power_name = f"⚡ CLAUDE-CODE RUST OVERDRIVE (Power #{power_id})"
        else:
            power_name = f"🛡️ MUTATION IMPERVIOUS SHIELD (Power #{power_id})"
        return 42.0, 2.5, power_name, power_id, True

    elif timeout_pct < 0.60:
        power_id = random.randint(4000, 9999)
        if hero_key == "sofia":
            power_name = f"🔮 Ollama Deep Thinking Burst (Power #{power_id})"
        elif hero_key == "lucas":
            power_name = f"🚀 AGY Multi-Thread Surge (Power #{power_id})"
        else:
            power_name = f"🔰 Zero-Trust Barrier (Power #{power_id})"
        return 28.0, 1.2, power_name, power_id, False

    else:
        power_id = random.randint(1, 3999)
        if hero_key == "sofia":
            power_name = f"✨ Gemma Fast Inference (Power #{power_id})"
        elif hero_key == "lucas":
            power_name = f"⚙️ Claude-Code Turbo Synthesizer (Power #{power_id})"
        else:
            power_name = f"🧪 Automated Test Suite (Power #{power_id})"
        return 18.0, 0.0, power_name, power_id, False

# ============================================================
# GAME LOOP (PEGA -> AVISA -> BRANCH -> CODA -> COMMIT & PUSH -> MOVE & MERGE)
# ============================================================
async def dynamic_frenzy_and_training_game_loop():
    await asyncio.sleep(2)
    
    while True:
        if game_state.get("victory") or game_state.get("boss_hp", 0) <= 0:
            stage = game_state.get("boss_stage", 1) + 1
            game_state["boss_stage"] = stage
            game_state["boss_max_hp"] = 1000 + (stage * 500)
            game_state["boss_hp"] = game_state["boss_max_hp"]
            game_state["boss_name"] = f"PO EVIL BOSS (STAGE {stage})"
            game_state["victory"] = False
            game_state["boss_phase"] = f"🔥 PO VILÃO EVOLUIU PARA O ESTÁGIO {stage}! HP: {game_state['boss_max_hp']}!"
            audit_logs.append({
                "event_id": f"evt_{len(audit_logs)+1}",
                "action": "PO_BOSS_EVOLVED",
                "stage": stage,
                "max_hp": game_state["boss_max_hp"]
            })
            await asyncio.sleep(3)

        # FASE 1: ACADEMIA DOS HERÓIS
        backlog_size = len(game_state["kanban"]["to_do"])
        training_time = 120 if backlog_size < 5 else 10
        
        game_state["current_phase"] = "HERO_TRAINING_PHASE"
        game_state["boss_phase"] = f"🎓 ACADEMIA GITHUB (STAGE {game_state.get('boss_stage', 1)}): HERÓIS APRENDENDO E COMMITANDO!"
        game_state["duel"]["is_active"] = False

        for sec in range(training_time, 0, -1):
            game_state["phase_timer_sec"] = sec
            if sec % 8 == 0:
                hero_k = random.choice(["felipe", "sofia", "lucas", "beatriz"])
                new_skill = learn_new_skills_autonomously(hero_k)
                asyncio.create_task(_do_real_commit(hero_k, new_skill))
            await asyncio.sleep(1.0)

        # FASE 2: PO FRENZY MODE
        game_state["current_phase"] = "PO_FRENZY_30S"
        game_state["boss_phase"] = f"⚡ PO FRENZY (STAGE {game_state.get('boss_stage', 1)})! VILÃO CRIANDO CARDS NO JIRA!"
        game_state["boss_cards_created_in_frenzy"] = 0
        
        frenzy_time = 30 if backlog_size < 15 else 5

        for sec in range(frenzy_time, 0, -1):
            game_state["phase_timer_sec"] = sec
            if sec % 6 == 0:
                asyncio.create_task(create_real_jira_card_async())
            await asyncio.sleep(1.0)

        if len(game_state["kanban"]["to_do"]) < 4:
            for _ in range(4 - len(game_state["kanban"]["to_do"])):
                asyncio.create_task(create_real_jira_card_async())
            await asyncio.sleep(2.0)

        # FASE 3: HERÓIS CLEARING (FLUXO COMPLETO E RIGOROSO DE ENGENHARIA)
        total_backlog = len(game_state["kanban"]["to_do"])
        target_clear_count = max(1, int(total_backlog * 0.8)) if total_backlog > 0 else 1
        game_state["target_cards_to_clear_80pct"] = target_clear_count
        game_state["cards_cleared_in_current_wave"] = 0
        game_state["current_phase"] = "HEROES_CLEARING_PHASE"
        game_state["boss_phase"] = f"⚔️ HERÓIS BAIXANDO 80% ({target_clear_count} CARDS) COM VALIDAÇÃO DO PO VILÃO!"
        
        wave_max_timer = 180
        game_state["phase_timer_sec"] = wave_max_timer

        while game_state["cards_cleared_in_current_wave"] < target_clear_count and wave_max_timer > 0:
            if game_state.get("boss_hp", 100) <= 0: break

            wave_max_timer -= 1
            game_state["phase_timer_sec"] = wave_max_timer
            duel = game_state["duel"]

            # STEP 1: PEGAR O CARD DO TO_DO E OBTER BRIEFING TÉCNICO
            if not duel["is_active"] and game_state["kanban"]["to_do"]:
                card = game_state["kanban"]["to_do"].pop(0)
                card.setdefault("rejections", 0)
                card.setdefault("po_rejection_reason", "")
                
                assigned_hero_key, reason, action_plan = felipe_analyze_and_delegate_card(card)
                hero = pixel_agents[assigned_hero_key]

                pixel_agents["felipe"]["action"] = f"🧠 Orientou {hero['name']} p/ [{card['id']}]"

                game_state["duel"] = {
                    "is_active": True,
                    "active_hero": hero["name"],
                    "hero_key": assigned_hero_key,
                    "active_card": card,
                    "git_branch": None,
                    "work_progress": 0.0,
                    "timeout_timer_sec": hero["timeout_resistance_sec"],
                    "max_timeout_sec": hero["timeout_resistance_sec"],
                    "damage_dealt": 0,
                    "active_power": f"📋 BRIEFING: {reason}",
                    "phase": "picking"
                }
                
                game_state["boss_phase"] = f"📌 {hero['name'].upper()} PEGOU O CARD [{card['id']}]!"
                pixel_agents[assigned_hero_key]["action"] = f"📌 Pegou [{card['id']}]"
                
                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "HERO_PICKED_CARD",
                    "card_id": card["id"],
                    "assigned_to": hero["name"]
                })
                await asyncio.sleep(1.0)
                continue

            if not duel["is_active"] and not game_state["kanban"]["to_do"] and not game_state["kanban"]["in_progress"] and not game_state["kanban"]["in_validation"]:
                break

            if not duel["is_active"]:
                await asyncio.sleep(1.0)
                continue

            hero_key = duel["hero_key"]
            hero = pixel_agents[hero_key]
            card_duel = duel["active_card"]

            # STEP 2: AVISAR O QUE VAI FAZER & PUBLICAR BRIEFING NO JIRA
            if duel["phase"] == "picking":
                duel["phase"] = "announcing"
                intent_msg = f"📣 'Vou assumir [{card_duel['id']}]: {card_duel['title'][:30]}...'"
                pixel_agents[hero_key]["action"] = intent_msg
                duel["active_power"] = f"🗣️ AVISANDO: {intent_msg}"
                game_state["boss_phase"] = f"🗣️ {hero['name']}: {intent_msg}"
                
                action_plan_text = card_duel.get("action_plan", "Executar refatoração e testes.")
                comment_body = (
                    f"👔 **Felipe (Líder de Arquitetura)** analisou o card e orientou **{hero['name']}**:\n\n"
                    f"📌 **Motivo da Delegação:** {card_duel.get('delegation_note', '')}\n\n"
                    f"🎯 **O que precisa ser feito (Plano de Ação):**\n{action_plan_text}\n\n"
                    f"🚀 **Status:** Card atribuído. Herói iniciando criação de branch."
                )
                asyncio.create_task(safe_jira_comment(card_duel["id"], comment_body, "Felipe Architect"))

                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "HERO_ANNOUNCED_INTENT",
                    "hero": hero["name"],
                    "card_id": card_duel["id"]
                })
                await asyncio.sleep(1.2)
                duel["phase"] = "creating_branch"
                continue

            # STEP 3: CRIAR A GIT FEATURE BRANCH
            if duel["phase"] == "creating_branch":
                branch_name = await create_git_feature_branch(card_duel["id"], hero["name"])
                duel["git_branch"] = branch_name
                
                card_duel["status"] = "EM PROGRESSO"
                if card_duel not in game_state["kanban"]["in_progress"]:
                    game_state["kanban"]["in_progress"].append(card_duel)

                if str(card_duel["id"]).startswith("KAN-"):
                    asyncio.create_task(asyncio.to_thread(jira.transition_issue, card_duel["id"], "In Progress"))

                msg_branch = f"🌿 Git Branch criada: {branch_name}"
                pixel_agents[hero_key]["action"] = msg_branch
                duel["active_power"] = msg_branch
                game_state["boss_phase"] = f"🌿 {hero['name']} criou a branch `{branch_name}`!"

                comment_branch = f"🌿 **Git Branch Criada:** `{branch_name}`\nCard movido para **Em Progresso**."
                asyncio.create_task(safe_jira_comment(card_duel["id"], comment_branch, hero["name"]))

                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "GIT_BRANCH_CREATED",
                    "card_id": card_duel["id"],
                    "branch": branch_name
                })
                await asyncio.sleep(1.2)
                duel["phase"] = "coding"
                continue

            # STEP 4: CODIFICAR E AVANÇAR PROGRESSO
            if duel["phase"] == "coding":
                duel["timeout_timer_sec"] = round(duel["timeout_timer_sec"] - 1.0, 1)
                timeout_pct = max(0.0, duel["timeout_timer_sec"] / duel["max_timeout_sec"])

                progress_boost, time_restore, power_name, power_id, shield_active = trigger_hero_timeout_power(hero_key, timeout_pct)

                if shield_active:
                    card_duel["shield_active"] = True

                if time_restore > 0:
                    duel["timeout_timer_sec"] = min(hero["timeout_resistance_sec"], round(duel["timeout_timer_sec"] + time_restore, 1))

                duel["work_progress"] = min(100.0, round(duel.get("work_progress", 0.0) + progress_boost, 1))
                duel["active_power"] = power_name
                pixel_agents[hero_key]["action"] = f"💻 Codando [{card_duel['id']}] ({duel['work_progress']}%)"

                if duel["work_progress"] >= 100.0 and duel["timeout_timer_sec"] > 0:
                    duel["phase"] = "submitting_commit"
                    pixel_agents[hero_key]["action"] = f"⚡ Finalizando código na branch..."
                    await asyncio.sleep(0.5)
                    continue

                elif duel["timeout_timer_sec"] <= 0:
                    card_duel["rejections"] += 1
                    card_duel["status"] = "A FAZER"
                    card_duel["po_rejection_reason"] = "⏰ TIMEOUT! Herói não terminou a tempo!"
                    if card_duel in game_state["kanban"]["in_progress"]:
                        game_state["kanban"]["in_progress"].remove(card_duel)
                    game_state["kanban"]["to_do"].append(card_duel)
                    
                    if str(card_duel["id"]).startswith("KAN-"):
                        asyncio.create_task(asyncio.to_thread(jira.transition_issue, card_duel["id"], "To Do"))
                        
                    comment_timeout = f"⏰ **TIMEOUT:** O herói **{hero['name']}** excedeu o limite de tempo na branch `{duel.get('git_branch')}`.\nCard devolvido para **A Fazer**."
                    asyncio.create_task(safe_jira_comment(card_duel["id"], comment_timeout, "System Governance"))

                    game_state["boss_phase"] = f"💀 {hero['name']} FALHOU NO TIMEOUT! [{card_duel['id']}] volta ao A FAZER!"
                    duel["is_active"] = False
                    duel["phase"] = "idle"
                    pixel_agents[hero_key]["action"] = f"😰 TIMEOUT! Card [{card_duel['id']}] retornou!"

            # STEP 5: COMMIT, PUSH E MOVER PARA VALIDAÇÃO
            elif duel["phase"] == "submitting_commit":
                game_state["boss_phase"] = f"⚙️ COMMITTANDO & ENVIANDO PUSH NA BRANCH `{duel.get('git_branch')}`..."
                
                commit_res = await synthesize_and_commit_real_code(hero["name"], card_duel["title"], card_duel["id"])
                card_duel["commit_info"] = commit_res
                
                branch_name = duel.get("git_branch")
                if branch_name:
                    await asyncio.to_thread(
                        subprocess.run,
                        ["git", "push", "-u", "origin", branch_name],
                        cwd=REPO_PATH, capture_output=True, text=True
                    )
                
                commit_msg = commit_res.get("commit_msg", "")
                hero["github_commits"].append(commit_msg)
                if commit_res.get("file_path"):
                    hero["github_commits"].append(f"📄 {commit_res['file_path']} (+{commit_res.get('lines_added', 0)} linhas)")

                card_duel["status"] = "EM VALIDAÇÃO"
                if card_duel in game_state["kanban"]["in_progress"]:
                    game_state["kanban"]["in_progress"].remove(card_duel)
                game_state["kanban"]["in_validation"].append(card_duel)
                
                if str(card_duel["id"]).startswith("KAN-"):
                    asyncio.create_task(asyncio.to_thread(jira.transition_issue, card_duel["id"], "In Validation"))

                comment_commit = (
                    f"🤖 **{hero['name']}** concluiu a implementação com sucesso!\n\n"
                    f"🌿 **Branch:** `{duel.get('git_branch', 'main')}`\n"
                    f"🐙 **Commit Git:** `{commit_res.get('commit_hash', 'HEAD')}`\n"
                    f"📄 **Módulo Gerado:** `{commit_res.get('file_path', 'código')}` (+{commit_res.get('lines_added', 0)} linhas)\n"
                    f"🧪 **Pytest:** {'✅ Passou' if commit_res.get('test_passed') else '❌ Falhou'}\n\n"
                    f"Card movido para **Em Validação**."
                )
                asyncio.create_task(safe_jira_comment(card_duel["id"], comment_commit, hero["name"]))
                    
                duel["phase"] = "in_validation"
                duel["timeout_timer_sec"] = 6.0
                duel["max_timeout_sec"] = 6.0
                game_state["boss_phase"] = f"🔍 CARD [{card_duel['id']}] MOVIDO PARA VALIDAÇÃO! PO VILÃO INSPECCIONANDO GIT..."
                pixel_agents[hero_key]["action"] = f"📤 Moveu [{card_duel['id']}] para Validação!"
                await asyncio.sleep(1.0)

            # STEP 6: PO VILÃO AUDITA O COMMIT NO GIT REAL E REALIZA O MERGE
            elif duel["phase"] == "in_validation":
                duel["timeout_timer_sec"] = round(duel["timeout_timer_sec"] - 1.0, 1)

                if duel["timeout_timer_sec"] <= 0:
                    commit_info = card_duel.get("commit_info", {})
                    
                    # 1. PO Vilão inspeciona o commit diretamente na FEATURE BRANCH
                    approved, reason = await po_vilao_inspect_commit_code_async(card_duel, commit_info)
                    
                    if approved:
                        branch_name = duel.get("git_branch")
                        
                        # 2. 🔀 MERGE AUTOMÁTICO DA FEATURE BRANCH NA MAIN & PUSH
                        if branch_name:
                            try:
                                await asyncio.to_thread(subprocess.run, ["git", "checkout", "main"], cwd=REPO_PATH, capture_output=True, text=True)
                                await asyncio.to_thread(subprocess.run, ["git", "merge", branch_name, "--no-ff", "-m", f"merge: {branch_name} into main [approved by PO]"], cwd=REPO_PATH, capture_output=True, text=True)
                                await asyncio.to_thread(subprocess.run, ["git", "push", "origin", "main"], cwd=REPO_PATH, capture_output=True, text=True)
                                print(f"[Git Merge] Branch {branch_name} mesclada na MAIN com sucesso!")
                            except Exception as e:
                                print(f"[Git Merge Error] Falha ao fazer merge de {branch_name}: {e}")

                        card_duel["status"] = "CONCLUÍDO"
                        card_duel["po_rejection_reason"] = reason
                        if card_duel in game_state["kanban"]["in_validation"]:
                            game_state["kanban"]["in_validation"].remove(card_duel)
                        game_state["kanban"]["done"].append(card_duel)
                        game_state["cards_cleared_in_current_wave"] += 1
                        game_state["cards_coded_count"] += 1
                        
                        if str(card_duel["id"]).startswith("KAN-"):
                            asyncio.create_task(asyncio.to_thread(jira.transition_issue, card_duel["id"], "Done"))

                        comment_done = (
                            f"✅ **PO EVIL BOSS:** Commit `{commit_info.get('commit_hash', '')}` auditado na branch `{branch_name}` e **APROVADO**!\n\n"
                            f"🔀 **Git Merge:** Código mesclado com sucesso na branch `main` e enviado ao repositório remoto.\n"
                            f"💬 **Parecer:** {reason}\n"
                            f"Card movido para **Concluído (Done)**."
                        )
                        asyncio.create_task(safe_jira_comment(card_duel["id"], comment_done, "PO Evil Boss"))

                        damage = 280 + (hero["skill_level"] * 20)
                        game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                        
                        game_state["boss_phase"] = f"✅ PO APROVOU [{card_duel['id']}]! MERGE NA MAIN REALIZADO! -{damage}HP!"
                        pixel_agents[hero_key]["action"] = f"🎉 Card [{card_duel['id']}] APROVADO & MERGED!"
                        
                        audit_logs.append({
                            "event_id": f"evt_{len(audit_logs)+1}",
                            "action": "PO_APPROVED_AND_MERGED_TO_MAIN",
                            "hero": hero["name"],
                            "card_id": card_duel["id"],
                            "branch": branch_name,
                            "damage": damage
                        })
                        
                        duel["is_active"] = False
                        duel["phase"] = "idle"
                        
                        if game_state["boss_hp"] <= 0:
                            game_state["victory"] = True
                            game_state["boss_phase"] = "🏆 VITÓRIA! HERÓIS DERROTARAM O PO VILÃO!"
                    else:
                        card_duel["rejections"] += 1
                        card_duel["status"] = "A FAZER"
                        card_duel["po_rejection_reason"] = f"{reason}"
                        if card_duel in game_state["kanban"]["in_validation"]:
                            game_state["kanban"]["in_validation"].remove(card_duel)
                        game_state["kanban"]["to_do"].append(card_duel)
                        
                        if str(card_duel["id"]).startswith("KAN-"):
                            asyncio.create_task(asyncio.to_thread(jira.transition_issue, card_duel["id"], "To Do"))
                        
                        comment_reject = (
                            f"🚫 **PO EVIL BOSS:** Commit `{commit_info.get('commit_hash', '')}` **REJEITADO NA AUDITORIA DO GIT**!\n\n"
                            f"💬 **Motivo:** {reason}\n"
                            f"Card retornado para **A Fazer** sem merge."
                        )
                        asyncio.create_task(safe_jira_comment(card_duel["id"], comment_reject, "PO Evil Boss"))

                        game_state["boss_phase"] = f"🚫 PO BARRATION! Commit de [{card_duel['id']}] REJEITADO! Devolvido ao A FAZER."
                        pixel_agents[hero_key]["action"] = f"💢 Commit [{card_duel['id']}] REJEITADO! Devolvido ao A FAZER!"
                        
                        audit_logs.append({
                            "event_id": f"evt_{len(audit_logs)+1}",
                            "action": "PO_REJECTED_GIT_COMMIT",
                            "hero": hero["name"],
                            "card_id": card_duel["id"],
                            "reason": reason[:65]
                        })
                        
                        duel["is_active"] = False
                        duel["phase"] = "idle"

            await asyncio.sleep(1.0)

        if not game_state["victory"]:
            game_state["boss_phase"] = f"🔄 WAVE CONCLUÍDA! {game_state['cards_cleared_in_current_wave']}/{target_clear_count} cards. Próxima rodada..."
            await asyncio.sleep(3)

async def _do_real_commit(hero_key: str, topic: str, card_id: Optional[str] = None):
    hero = pixel_agents[hero_key]
    res = await synthesize_and_commit_real_code(hero["name"], topic, card_id)
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

@app.on_event("startup")
async def start_autonomous_loop():
    await bus.start()
    asyncio.create_task(auto_save_persistence_loop())
    asyncio.create_task(dynamic_frenzy_and_training_game_loop())

@app.on_event("shutdown")
async def shutdown_event():
    await bus.stop()

@app.get("/api/boss/state")
async def get_boss_state():
    for agent in pixel_agents.values():
        agent["x"] += random.choice([-2, 0, 2])
        agent["y"] += random.choice([-2, 0, 2])
        agent["x"] = max(50, min(550, agent["x"]))
        agent["y"] = max(200, min(320, agent["y"]))

    return {
        "game_state": game_state,
        "pixel_agents": list(pixel_agents.values()),
        "duel": game_state["duel"],
        "kanban": game_state["kanban"],
        "audit_logs": audit_logs[-8:],
    }

@app.get("/", response_class=HTMLResponse)
async def serve_autonomous_pixel_game():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE AEOS — GitHub Skill Commit Engine</title>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                background: #0d0e15;
                color: #fff;
                font-family: 'Press Start 2P', monospace;
                overflow: hidden;
            }

            #game-container {
                display: flex;
                width: 100vw;
                height: 100vh;
            }

            #pixel-canvas {
                background: #181926;
                border-right: 4px solid #3b3d54;
                image-rendering: pixelated;
                flex-shrink: 0;
            }

            .side-panel {
                flex: 1;
                background: #11121d;
                padding: 1rem;
                display: flex;
                flex-direction: column;
                gap: 0.6rem;
                border-left: 4px solid #3b3d54;
                overflow-y: auto;
            }

            .hud-title {
                font-size: 0.6rem;
                color: #55ff55;
                text-shadow: 2px 2px #00aa00;
                text-align: center;
                padding: 0.4rem;
                border-bottom: 2px solid #1f2040;
            }

            .turn-banner {
                background: rgba(168, 85, 247, 0.15);
                border: 2px solid #a855f7;
                border-radius: 6px;
                padding: 0.5rem 0.8rem;
                text-align: center;
                font-size: 0.48rem;
                line-height: 1.6;
            }

            .duel-arena-box {
                background: rgba(59, 130, 246, 0.1);
                border: 2px solid #3b82f6;
                border-radius: 8px;
                padding: 0.7rem;
            }

            .duel-timer-bg {
                width: 100%;
                height: 16px;
                background: #440000;
                border: 2px solid #ff5555;
                border-radius: 4px;
                margin-top: 0.4rem;
                overflow: hidden;
                position: relative;
            }

            .duel-timer-fill {
                height: 100%;
                background: linear-gradient(90deg, #00ff00, #55ff55);
                transition: width 0.9s linear;
            }

            .kanban-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 0.4rem;
            }

            .kanban-col {
                background: rgba(0,0,0,0.6);
                border: 2px solid #30363d;
                border-radius: 6px;
                padding: 0.4rem;
                height: 270px;
                display: flex;
                flex-direction: column;
            }

            .kanban-col-cards {
                flex: 1;
                overflow-y: auto;
                padding-right: 0.2rem;
            }

            .kanban-col-cards::-webkit-scrollbar { width: 4px; }
            .kanban-col-cards::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 2px; }

            .kanban-col-title {
                font-size: 0.37rem;
                font-weight: bold;
                margin-bottom: 0.3rem;
                text-align: center;
                padding-bottom: 0.2rem;
                border-bottom: 1px solid #30363d;
            }

            .card-todo { color: #ff5555; border-color: #ff5555; }
            .card-progress { color: #60a5fa; border-color: #60a5fa; }
            .card-validation { color: #ffaa00; border-color: #ffaa00; }
            .card-done { color: #55ff55; border-color: #55ff55; }

            .kanban-card-item {
                background: rgba(255,255,255,0.05);
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 0.3rem;
                margin-bottom: 0.3rem;
                font-size: 0.34rem;
                line-height: 1.4;
            }

            .kanban-card-item.active-card {
                border-color: #60a5fa;
                background: rgba(59, 130, 246, 0.12);
                animation: pulse-card 1s ease-in-out infinite alternate;
            }

            .kanban-card-item.rejected-card {
                border-color: #ff5555;
                background: rgba(255, 85, 85, 0.08);
            }

            @keyframes pulse-card {
                from { box-shadow: 0 0 4px rgba(59,130,246,0.3); }
                to { box-shadow: 0 0 10px rgba(59,130,246,0.8); }
            }

            .github-commit-item {
                color: #60a5fa;
                font-size: 0.34rem;
                margin-top: 0.2rem;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            .real-commit-badge {
                background: rgba(34, 197, 94, 0.2);
                border: 1px solid #22c55e;
                color: #22c55e;
                font-size: 0.32rem;
                padding: 0.1rem 0.3rem;
                border-radius: 3px;
                display: inline-block;
                margin-left: 0.2rem;
            }

            .audit-log-entry {
                font-size: 0.36rem;
                color: #9ca3af;
                margin-bottom: 0.2rem;
                line-height: 1.4;
            }

            .audit-approved { color: #55ff55; }
            .audit-rejected { color: #ff5555; }
            .audit-commit { color: #60a5fa; }
            .audit-jira { color: #a855f7; }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>

            <div class="side-panel">
                <div class="hud-title">⚡ FLOSE AEOS — KANBAN DUELO COM PO VILÃO & COMMITS REAIS GITHUB</div>

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
                        🐙 COMMITS REAIS NO GITHUB 
                        <span id="commit-count" style="color:#22c55e; font-size:0.38rem;"></span>
                    </div>
                    <div id="skills-list">Carregando heróis...</div>
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
                    const actionText = action.substring(0, 28);
                    ctx.fillText(actionText, x - 20, y - 3);
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

            function drawPOBoss(hpPercent, phaseText, phase) {
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

                ctx.fillStyle = "#ff0000";
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
                ctx.fillRect(hpBarX, 12, (hpBarW * hpPercent) / 100, 18);
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = 2;
                ctx.strokeRect(hpBarX, 12, hpBarW, 18);

                ctx.font = '6px "Press Start 2P"';
                ctx.fillStyle = "#ffffff";
                ctx.fillText(`HP: ${Math.round(hpPercent)}%`, hpBarX + 4, 25);

                ctx.font = '5px "Press Start 2P"';
                ctx.fillStyle = "#ffaa00";
                const phaseShort = phaseText ? phaseText.substring(0, 55) : "";
                ctx.fillText(phaseShort, canvas.width / 2 - 160, by + 120 + bossAnim);
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

                if (gameState) {
                    const hpPct = (gameState.boss_hp / gameState.boss_max_hp) * 100;
                    drawPOBoss(hpPct, gameState.boss_phase || "", gameState.current_phase);

                    agentsList.forEach(a => {
                        const isDuelist = duelState && duelState.is_active && duelState.active_hero === a.name;
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, isDuelist, a.skill_level, a.action);
                    });

                    ctx.font = '8px "Press Start 2P"';
                    ctx.fillStyle = "#55ff55";
                    const timerText = `⏱️ ${gameState.phase_timer_sec}s`;
                    ctx.fillText(timerText, canvas.width / 2 - 30, canvas.height - 20);
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

                    const phase = gameState.current_phase;
                    const banner = document.getElementById('turn-banner');
                    if (phase === "HERO_TRAINING_PHASE") {
                        banner.style.borderColor = "#a855f7";
                        banner.style.color = "#a855f7";
                        banner.innerHTML = `🎓 ACADEMIA GITHUB: COMMITANDO SKILLS REAIS | ⏱️ ${gameState.phase_timer_sec}s`;
                    } else if (phase === "PO_FRENZY_30S") {
                        banner.style.borderColor = "#ff5555";
                        banner.style.color = "#ff5555";
                        banner.innerHTML = `🔥 PO FRENZY! VILÃO CRIANDO CARDS NO JIRA | ⏱️ ${gameState.phase_timer_sec}s`;
                    } else {
                        banner.style.borderColor = "#55ff55";
                        banner.style.color = "#55ff55";
                        banner.innerHTML = `⚔️ HERÓIS BAIXANDO 80%: ${gameState.cards_cleared_in_current_wave}/${gameState.target_cards_to_clear_80pct} CARDS | ⏱️ ${gameState.phase_timer_sec}s`;
                    }

                    const duel = duelState;
                    if (duel && duel.is_active && duel.active_card) {
                        const pct = Math.max(0, (duel.timeout_timer_sec / duel.max_timeout_sec) * 100);
                        const timerColor = pct < 30 ? '#ff5555' : pct < 60 ? '#ffaa00' : '#00ff00';
                        
                        let phaseLabel = "💻 HERÓI EM AÇÃO";
                        let phaseColor = "#60a5fa";

                        if (duel.phase === "picking") {
                            phaseLabel = "📌 1. PEGANDO CARD DO TO-DO";
                            phaseColor = "#a855f7";
                        } else if (duel.phase === "announcing") {
                            phaseLabel = "📣 2. AVISANDO PLANO & JIRA";
                            phaseColor = "#ec4899";
                        } else if (duel.phase === "creating_branch") {
                            phaseLabel = "🌿 3. CRIANDO GIT BRANCH";
                            phaseColor = "#10b981";
                        } else if (duel.phase === "coding") {
                            phaseLabel = `💻 4. ENTENDENDO & CODANDO (${duel.work_progress || 0}%)`;
                            phaseColor = "#60a5fa";
                        } else if (duel.phase === "submitting_commit") {
                            phaseLabel = "⚙️ 5. SINTETIZANDO CÓDIGO E COMMITANDO";
                            phaseColor = "#f97316";
                        } else if (duel.phase === "in_validation") {
                            phaseLabel = "🔍 6. MOVIDO! PO VILÃO AUDITANDO COMMIT";
                            phaseColor = "#ffaa00";
                        }
                        
                        document.getElementById('duel-box').innerHTML = `
                            <div style="font-size:0.52rem; color:${phaseColor}; font-weight:bold; margin-bottom:0.25rem; text-align:center;">
                                ${phaseLabel}
                            </div>
                            <div style="font-size:0.44rem; color:#3b82f6; margin-bottom:0.2rem;">
                                👔 <b>Felipe:</b> Delegou para <span style="color:#a855f7;">${duel.active_hero}</span>!
                            </div>
                            <div style="font-size:0.46rem; color:#fff; margin-bottom:0.2rem;">
                                ⚔️ <b>Herói:</b> <span style="color:#a855f7;">${duel.active_hero}</span> — Card: <span style="color:#ec4899;">[${duel.active_card.id}]</span>
                            </div>
                            ${duel.git_branch ? `<div style="font-size:0.38rem; color:#10b981; margin-bottom:0.2rem;">🌿 Branch: <code>${duel.git_branch}</code></div>` : ''}
                            <div style="font-size:0.42rem; color:#55ff55; font-weight:bold; margin-bottom:0.25rem;">
                                ${duel.active_power || 'Acionando Habilidade...'}
                            </div>
                            <div style="font-size:0.38rem; color:#9ca3af; margin-bottom:0.25rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                ${duel.active_card.title ? duel.active_card.title.substring(0, 45) + '...' : ''}
                            </div>
                            ${duel.active_card.po_rejection_reason ? `<div style="font-size:0.38rem; color:#ff5555; margin-bottom:0.2rem;">💬 ${duel.active_card.po_rejection_reason.substring(0, 50)}</div>` : ''}
                            <div style="font-size:0.42rem; color:${timerColor}; font-weight:bold; margin-bottom:0.2rem;">
                                ⏱️ TIMEOUT: ${typeof duel.timeout_timer_sec === 'number' ? duel.timeout_timer_sec.toFixed(1) : '??'}s 
                                (${duel.active_card.rejections || 0} rejeição/ões)
                            </div>
                            <div class="duel-timer-bg">
                                <div class="duel-timer-fill" style="width:${pct}%; background:${timerColor};"></div>
                            </div>
                        `;
                    } else {
                        const idleMsg = phase === "HERO_TRAINING_PHASE"
                            ? "🎓 HERÓIS CRIANDO COMMITS REAIS NO GITHUB!"
                            : phase === "PO_FRENZY_30S"
                            ? "🔥 PO VILÃO NO FRENZY MODE — CRIANDO CARDS NO JIRA!"
                            : "😴 AGUARDANDO PRÓXIMO CARD...";
                        document.getElementById('duel-box').innerHTML = `
                            <div style="font-size:0.46rem; color:#9ca3af; text-align:center; padding:0.5rem;">${idleMsg}</div>
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
                        if (!cards || cards.length === 0) {
                            return '<div style="font-size:0.32rem; color:#4b5563; text-align:center; padding:0.8rem 0;">Nenhum card</div>';
                        }
                        return cards.map(c => {
                            const isActive = c.id === activeCardId;
                            const isRejected = c.rejections > 0;
                            const jiraUrl = `https://felipeflose.atlassian.net/browse/${c.id}`;
                            const titleFull = c.title || '';
                            const titleDisplay = titleFull.length > 30 ? titleFull.substring(0, 27) + '...' : titleFull;
                            const commitHash = c.commit_info ? c.commit_info.commit_hash : null;
                            
                            return `
                                <div class="kanban-card-item ${isActive ? 'active-card' : ''} ${isRejected && !isActive ? 'rejected-card' : ''}">
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.15rem;">
                                        <a href="${jiraUrl}" target="_blank" style="color:${colorClass}; font-weight:bold; font-size:0.38rem; text-decoration:underline;" title="Abrir card no Jira Cloud">
                                            ${c.id} 🔗
                                        </a>
                                        ${commitHash ? `<span style="font-size:0.3rem; color:#60a5fa; background:rgba(96,165,250,0.15); padding:0.05rem 0.2rem; border-radius:3px;">🐙 ${commitHash}</span>` : ''}
                                    </div>
                                    <div style="font-size:0.34rem; color:#e5e7eb; line-height:1.3; margin-bottom:0.2rem;" title="${titleFull}">
                                        ${titleDisplay}
                                    </div>
                                    ${c.delegated_to ? `<div style="font-size:0.31rem; color:#3b82f6; margin-bottom:0.15rem;">👔 → <span style="color:#a855f7;">${c.delegated_to}</span></div>` : ''}
                                    ${c.po_rejection_reason ? `<div style="color:#ff5555; font-size:0.3rem; margin-top:0.1rem;" title="${c.po_rejection_reason}">💬 ${c.po_rejection_reason.substring(0, 42)}</div>` : ''}
                                    ${c.rejections > 0 && !c.po_rejection_reason ? `<div style="color:#ff5555; font-size:0.3rem;">⚠️ ${c.rejections}x rejeitado</div>` : ''}
                                </div>
                            `;
                        }).join('');
                    }

                    document.getElementById('col-todo').innerHTML = renderCards(todoCards, '#ff5555');
                    document.getElementById('col-progress').innerHTML = renderCards(progressCards, '#60a5fa');
                    document.getElementById('col-validation').innerHTML = renderCards(validationCards, '#ffaa00');
                    document.getElementById('col-done').innerHTML = renderCards(doneCards, '#55ff55');

                    const commitCount = gameState.total_real_commits || 0;
                    document.getElementById('commit-count').textContent = `(${commitCount} commits reais ✅)`;

                    document.getElementById('skills-list').innerHTML = agentsList.map(a => {
                        const recentCommits = (a.github_commits || []).slice(-2);
                        const commitsHtml = recentCommits.map(c => {
                            const isReal = !c.includes('[skip]') && !c.includes('[erro]');
                            return `<div class="github-commit-item">
                                🐙 ${c.substring(0, 48)}
                                ${isReal ? '<span class="real-commit-badge">REAL</span>' : ''}
                            </div>`;
                        }).join('');
                        return `
                            <div style="background:rgba(0,0,0,0.5); border:1px solid #30363d; padding:0.35rem; border-radius:4px; margin-bottom:0.25rem;">
                                <div style="color:${a.sprite_color}; font-weight:bold; font-size:0.4rem;">
                                    ${a.name} (Lv.${a.skill_level}) 
                                    <span style="color:#a855f7; float:right;">XP: ${a.xp || 0}%</span>
                                </div>
                                <div style="color:#55ff55; font-size:0.35rem; margin-top:0.15rem;">
                                    🧠 ${(a.new_skills_learned || []).slice(-2).join(', ')}
                                </div>
                                ${commitsHtml}
                            </div>
                        `;
                    }).join('');

                    document.getElementById('audit-log').innerHTML = auditLogs.map(l => {
                        let cls = 'audit-log-entry';
                        if (l.action === 'PO_APPROVED_AND_MERGED_TO_MAIN') cls += ' audit-approved';
                        else if (l.action === 'PO_REJECTED_GIT_COMMIT') cls += ' audit-rejected';
                        else if (l.action === 'GIT_BRANCH_CREATED') cls += ' audit-commit';
                        else if (l.action && l.action.includes('JIRA')) cls += ' audit-jira';
                        
                        const detail = l.reason || l.commit || l.card_id || l.hero || l.branch || '';
                        return `<div class="${cls}">» [${l.action}] ${detail.substring(0, 55)}</div>`;
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