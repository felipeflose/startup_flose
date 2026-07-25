import asyncio
import time
import random
import os
import subprocess
import json
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

app = FastAPI(title="FLOSE AEOS - Real GitHub Skill Commit Engine")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

REPO_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILLS_DOC_PATH = os.path.join(REPO_PATH, "docs", "skills_learned.md")

# Busca os cards REAIS do Jira Cloud da sua conta (felipeflose.atlassian.net)
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=10)
for c in real_jira_cards:
    c.setdefault("rejections", 0)

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

# HERÓIS COM REGISTRO DE COMMITS REAIS NO GITHUB DE CADA SKILL APRENDIDA
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

# ============================================================
# REAL GITHUB COMMIT ENGINE
# ============================================================
_git_commit_lock = asyncio.Lock()

async def push_real_github_skill_commit(agent_name: str, skill_name: str) -> str:
    """Faz um commit REAL no GitHub com a nova skill aprendida."""
    async with _git_commit_lock:
        try:
            # Cria o arquivo docs/skills_learned.md
            os.makedirs(os.path.dirname(SKILLS_DOC_PATH), exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"- [{timestamp}] [{agent_name}] aprendeu: **{skill_name}**\n"
            
            with open(SKILLS_DOC_PATH, "a", encoding="utf-8") as f:
                f.write(entry)

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
# JIRA CARD CREATION (BACKGROUND)
# ============================================================
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
# VILÃO VALIDA OS CARDS (PO REVIEW)
# ============================================================
PO_REJECTION_REASONS = [
    "Falta critério de aceite detalhado!",
    "Sem evidência de teste unitário!",
    "Estimativa em story points ausente!",
    "Descrição muito vaga, reescreva!",
    "Sem link para épico pai!",
    "A implementação viola nosso padrão de arquitetura!",
    "Nenhum cenário de borda documentado!",
    "Falta definição de 'Done' explícita!",
    "Sem aprovação de segurança XSS!",
    "Performance não foi validada com métricas!"
]

def po_vilao_review(card: Dict[str, Any]) -> tuple[bool, str]:
    """O PO Vilão revisa o card. Ele é muito chato — rejeita na maioria das vezes!"""
    rejection_chance = 0.55  # 55% de chance de rejeitar (vilão foi balanceado)
    card_rejections = card.get("rejections", 0)
    # A cada rejeição prévia ou se teve escudo ativado, diminui a chance de rejeição
    if card.get("shield_active"):
        rejection_chance = 0.05  # Escudo QA/Security garante aprovação!
    else:
        rejection_chance = max(0.15, rejection_chance - (card_rejections * 0.12))
    
    if random.random() < rejection_chance:
        reason = random.choice(PO_REJECTION_REASONS)
        return False, reason
    return True, "✅ Aprovado! Critérios de aceite atendidos."


# ============================================================
# FELIPE DELEGATION & HERO TIMEOUT POWER ENGINE (13.000 PODERES)
# ============================================================
def felipe_analyze_and_delegate_card(card: Dict[str, Any]) -> str:
    """
    Felipe (CEO/Architect) analisa a complexidade do card do Jira 
    e delega para o herói especialista ideal (Sofia, Lucas ou Beatriz)!
    """
    title_lower = ((card.get("title") or "") + " " + (card.get("description") or "")).lower()

    if any(k in title_lower for k in ["gemma", "ollama", "prompt", "ia", "analys", "fine-tuning", "modelo"]):
        assigned = "sofia"
        reason = "Felipe analisou: Requer análise profunda de IA com Gemma 4 & Ollama."
    elif any(k in title_lower for k in ["refator", "async", "perform", "rust", "backend", "cache", "speed"]):
        assigned = "lucas"
        reason = "Felipe analisou: Requer síntese de alta velocidade com Claude-Code & AGY."
    else:
        assigned = "beatriz"
        reason = "Felipe analisou: Requer suíte QA & sanitização estrita de segurança."

    card["delegated_by"] = "Felipe (Líder de Arquitetura)"
    card["delegated_to"] = pixel_agents[assigned]["name"]
    card["delegation_note"] = reason
    return assigned


def trigger_hero_timeout_power(hero_key: str, timeout_pct: float) -> Tuple[float, float, str, int, bool]:
    """
    Aciona um dos 13.000 Poderes do Herói baseado no nível do Timeout:
    - Tier 1 (>60% time): Habilidade Básica
    - Tier 2 (25% a 60% time): Habilidade Especial + Pequena regeneração de tempo
    - Tier 3 (<25% time): LIMIT BREAK DESESPERO (#1 a #13000) -> Avanço massivo e escudo!
    Retorna: (progress_boost, time_restore_sec, power_name, power_id, shield_active)
    """
    hero = pixel_agents[hero_key]

    if timeout_pct < 0.25:
        # TIER 3: LIMIT BREAK (<25% timeout)
        power_id = random.randint(10000, 13000)
        if hero_key == "sofia":
            power_name = f"🌟 GEMMA 4 QUANTUM BEAM (Power #{power_id})"
        elif hero_key == "lucas":
            power_name = f"⚡ CLAUDE-CODE RUST OVERDRIVE (Power #{power_id})"
        else:
            power_name = f"🛡️ MUTATION IMPERVIOUS SHIELD (Power #{power_id})"
        
        return 42.0, 2.5, power_name, power_id, True

    elif timeout_pct < 0.60:
        # TIER 2: SPECIAL SURGE (25% a 60% timeout)
        power_id = random.randint(4000, 9999)
        if hero_key == "sofia":
            power_name = f"🔮 Ollama Deep Thinking Burst (Power #{power_id})"
        elif hero_key == "lucas":
            power_name = f"🚀 AGY Multi-Thread Surge (Power #{power_id})"
        else:
            power_name = f"🔰 Zero-Trust Barrier (Power #{power_id})"
        
        return 28.0, 1.2, power_name, power_id, False

    else:
        # TIER 1: BASIC ATTACK (>60% timeout)
        power_id = random.randint(1, 3999)
        if hero_key == "sofia":
            power_name = f"✨ Gemma Fast Inference (Power #{power_id})"
        elif hero_key == "lucas":
            power_name = f"⚙️ Claude-Code Turbo Synthesizer (Power #{power_id})"
        else:
            power_name = f"🧪 Automated Test Suite (Power #{power_id})"
        
        return 18.0, 0.0, power_name, power_id, False

async def dynamic_frenzy_and_training_game_loop():
    await asyncio.sleep(2)  # Espera inicialização
    
    while True:
        # ==============================================================
        # FASE 1: ACADEMIA DOS HERÓIS (2 MINUTOS) - COMMITS REAIS GITHUB
        # ==============================================================
        game_state["current_phase"] = "HERO_TRAINING_PHASE"
        game_state["boss_phase"] = "🎓 ACADEMIA GITHUB: HERÓIS ESTUDANDO E COMMITANDO SKILLS REAIS!"
        game_state["duel"]["is_active"] = False

        for sec in range(120, 0, -1):
            if game_state["victory"]: break
            game_state["phase_timer_sec"] = sec

            if sec % 8 == 0:
                hero_k = random.choice(["felipe", "sofia", "lucas", "beatriz"])
                new_skill = learn_new_skills_autonomously(hero_k)
                
                # Faz o commit REAL no GitHub em background
                asyncio.create_task(_do_real_commit(hero_k, new_skill))

            await asyncio.sleep(1.0)

        if game_state["victory"]: break

        # ==============================================================
        # FASE 2: PO FRENZY MODE (30 SEGUNDOS - VILÃO CRIA CARDS NO JIRA)
        # ==============================================================
        game_state["current_phase"] = "PO_FRENZY_30S"
        game_state["boss_phase"] = "⚡ PO FRENZY! VILÃO CRIANDO CARDS NO JIRA REAL — 30 SEGUNDOS!"
        game_state["boss_cards_created_in_frenzy"] = 0

        po_topics_frenzy = [
            ("Refatorar UI Frontend Nível Pixel Perfect 16-Bit", "PO exige alinhamento HSL perfeito, zero bugs visuais em todas resoluções acima de 1024px. Critérios: Screenshot aprovado em 3 navegadores."),
            ("Otimização de Performance Backend Async & Caching", "Latência do EventBus < 5ms. Implementar cache Redis com TTL configurável. Critérios: Benchmark antes/depois documentado."),
            ("Auditoria Anti-Alucinação e Cobertura de Testes Mutation", "Testes de mutação com evidência SHA-256. Cobertura >= 90%. Critérios: Relatório Stryker exportado."),
            ("CONTRATAÇÃO: Onboarding de Desenvolvedor Frontend Senior", "Recrutar colaborador especialista em React/TypeScript. Critérios: CV analisado, entrevista técnica realizada, contrato assinado."),
            ("Sanitização Estrita contra Vulnerabilidades XSS & SQL", "Falhas de segurança nos endpoints REST. Critérios: Relatório OWASP ZAP sem críticos, PR aprovado com 2 revisores."),
        ]

        for sec in range(30, 0, -1):
            if game_state["victory"]: break
            game_state["phase_timer_sec"] = sec

            # A cada 6 segundos, cria um card no Jira
            if sec % 6 == 0:
                idx = game_state["boss_cards_created_in_frenzy"] % len(po_topics_frenzy)
                topic_title, topic_desc = po_topics_frenzy[idx]
                asyncio.create_task(async_create_jira_card_background(topic_title, topic_desc))

            await asyncio.sleep(1.0)

        if game_state["victory"]: break

        # ==============================================================
        # FASE 3: HERÓIS RESOLVEM 80% DOS CARDS (DUELO COMPLETO COM VALIDAÇÃO)
        # ==============================================================
        cards_created = max(1, game_state["boss_cards_created_in_frenzy"])
        target_clear_count = max(1, int(cards_created * 0.8))
        game_state["target_cards_to_clear_80pct"] = target_clear_count
        game_state["cards_cleared_in_current_wave"] = 0
        game_state["current_phase"] = "HEROES_CLEARING_PHASE"
        game_state["boss_phase"] = f"⚔️ HERÓIS BAIXANDO 80% ({target_clear_count} CARDS) COM VALIDAÇÃO DO PO VILÃO!"
        
        # Safety timeout para a onda inteira (180 segundos max)
        wave_max_timer = 180
        game_state["phase_timer_sec"] = wave_max_timer

        while game_state["cards_cleared_in_current_wave"] < target_clear_count and wave_max_timer > 0:
            if game_state["victory"]: break

            wave_max_timer -= 1
            game_state["phase_timer_sec"] = wave_max_timer
            duel = game_state["duel"]

            # ---- IDLE: pega um novo card do to_do ----
            if not duel["is_active"] and game_state["kanban"]["to_do"]:
                card = game_state["kanban"]["to_do"].pop(0)
                card.setdefault("rejections", 0)
                card.setdefault("po_rejection_reason", "")
                card["status"] = "EM PROGRESSO"
                game_state["kanban"]["in_progress"].append(card)

                # 🧠 FELIPE ANALISA E DELEGA PARA O HERÓI IDEAL (Sofia, Lucas ou Beatriz)
                assigned_hero_key = felipe_analyze_and_delegate_card(card)
                hero = pixel_agents[assigned_hero_key]

                # Felipe atualiza a ação dele no mapa
                pixel_agents["felipe"]["action"] = f"🧠 Analisou [{card['id']}] -> Delegou para {hero['name']}"

                game_state["duel"] = {
                    "is_active": True,
                    "active_hero": hero["name"],
                    "hero_key": assigned_hero_key,
                    "active_card": card,
                    "work_progress": 0.0,
                    "timeout_timer_sec": hero["timeout_resistance_sec"],
                    "max_timeout_sec": hero["timeout_resistance_sec"],
                    "damage_dealt": 0,
                    "active_power": "Inicializando Duelo...",
                    "phase": "hero_working"
                }
                
                game_state["boss_phase"] = f"👔 FELIPE DELEGOU [{card['id']}] PARA {hero['name'].upper()}!"
                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "FELIPE_DELEGATED_CARD",
                    "card_id": card["id"],
                    "assigned_to": hero["name"],
                    "note": card.get("delegation_note", "")
                })

                duel = game_state["duel"]

            # Se não há duel ativo nem cards no to_do/in_progress/in_validation, faz safety break
            if not duel["is_active"] and not game_state["kanban"]["to_do"] and not game_state["kanban"]["in_progress"] and not game_state["kanban"]["in_validation"]:
                print("[Safety Break] Nenhum card restante no Kanban. Finalizando onda.")
                break

            if not duel["is_active"]:
                await asyncio.sleep(1.0)
                continue

            hero_key = duel["hero_key"]
            hero = pixel_agents[hero_key]
            card_duel = duel["active_card"]

            # ---- FASE: hero_working ----
            if duel["phase"] == "hero_working":
                duel["timeout_timer_sec"] = round(duel["timeout_timer_sec"] - 1.0, 1)
                
                # Porcentagem de tempo de timeout restante
                timeout_pct = max(0.0, duel["timeout_timer_sec"] / duel["max_timeout_sec"])

                # ⚡ ACIONA UM DOS 13.000 PODERES BASEADO NO TIMEOUT!
                progress_boost, time_restore, power_name, power_id, shield_active = trigger_hero_timeout_power(hero_key, timeout_pct)

                if shield_active:
                    card_duel["shield_active"] = True

                if time_restore > 0:
                    duel["timeout_timer_sec"] = min(hero["timeout_resistance_sec"], round(duel["timeout_timer_sec"] + time_restore, 1))

                # Adiciona o boost do poder ao progresso do herói
                duel["work_progress"] = min(100.0, round(duel.get("work_progress", 0.0) + progress_boost, 1))
                duel["active_power"] = power_name
                
                hero_action_str = f"⚡ {power_name[:25]}: {duel['work_progress']}%"
                pixel_agents[hero_key]["action"] = hero_action_str

                # Quando atinge 100% de progresso antes do timeout -> vai para validação
                if duel["work_progress"] >= 100.0 and duel["timeout_timer_sec"] > 0:
                    card_duel["status"] = "EM VALIDAÇÃO"
                    if card_duel in game_state["kanban"]["in_progress"]:
                        game_state["kanban"]["in_progress"].remove(card_duel)
                    game_state["kanban"]["in_validation"].append(card_duel)
                    duel["phase"] = "in_validation"
                    duel["timeout_timer_sec"] = 6.0  # PO tem 6s para revisar
                    duel["max_timeout_sec"] = 6.0
                    game_state["boss_phase"] = f"🔍 {hero['name']} usou {power_name[:30]} e enviou [{card_duel['id']}] para PO Vilão!"
                    pixel_agents[hero_key]["action"] = f"📤 Card [{card_duel['id']}] em validação do PO!"

                elif duel["timeout_timer_sec"] <= 0:
                    # Timeout! Card volta ao A Fazer
                    card_duel["rejections"] += 1
                    card_duel["status"] = "A FAZER"
                    card_duel["po_rejection_reason"] = "⏰ TIMEOUT! Herói não terminou a tempo!"
                    if card_duel in game_state["kanban"]["in_progress"]:
                        game_state["kanban"]["in_progress"].remove(card_duel)
                    game_state["kanban"]["to_do"].append(card_duel)
                    game_state["boss_phase"] = f"💀 {hero['name']} FALHOU NO TIMEOUT! [{card_duel['id']}] volta ao A FAZER!"
                    duel["is_active"] = False
                    duel["phase"] = "idle"
                    pixel_agents[hero_key]["action"] = f"😰 TIMEOUT! Card [{card_duel['id']}] retornou!"

            # ---- FASE: in_validation (PO revisa) ----
            elif duel["phase"] == "in_validation":
                duel["timeout_timer_sec"] = round(duel["timeout_timer_sec"] - 1.0, 1)

                if duel["timeout_timer_sec"] <= 0:
                    # PO revisa o card
                    approved, reason = po_vilao_review(card_duel)
                    
                    if approved:
                        # APROVADO! Move para Done
                        card_duel["status"] = "CONCLUÍDO"
                        card_duel["po_rejection_reason"] = reason
                        if card_duel in game_state["kanban"]["in_validation"]:
                            game_state["kanban"]["in_validation"].remove(card_duel)
                        game_state["kanban"]["done"].append(card_duel)
                        game_state["cards_cleared_in_current_wave"] += 1
                        game_state["cards_coded_count"] += 1

                        damage = 280 + (hero["skill_level"] * 20)
                        game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                        
                        game_state["boss_phase"] = f"✅ PO APROVOU [{card_duel['id']}]! -{damage}HP do Vilão! ({game_state['cards_cleared_in_current_wave']}/{target_clear_count})"
                        pixel_agents[hero_key]["action"] = f"🎉 Card [{card_duel['id']}] APROVADO! Gerando código Python..."
                        
                        # Sintetiza módulo de código Python REAL e executa commit & push no GitHub!
                        asyncio.create_task(_do_real_commit(hero_key, card_duel["title"], card_duel["id"]))

                        audit_logs.append({
                            "event_id": f"evt_{len(audit_logs)+1}",
                            "action": "PO_APPROVED_REAL_CODE",
                            "hero": hero["name"],
                            "card_id": card_duel["id"],
                            "damage": damage
                        })
                        
                        duel["is_active"] = False
                        duel["phase"] = "idle"
                        
                        if game_state["boss_hp"] <= 0:
                            game_state["victory"] = True
                            game_state["boss_phase"] = "🏆 VITÓRIA! HERÓIS DERROTARAM O PO VILÃO!"
                    else:
                        # REJEITADO! Volta ao A Fazer com motivo
                        card_duel["rejections"] += 1
                        card_duel["status"] = "A FAZER"
                        card_duel["po_rejection_reason"] = f"❌ {reason}"
                        if card_duel in game_state["kanban"]["in_validation"]:
                            game_state["kanban"]["in_validation"].remove(card_duel)
                        game_state["kanban"]["to_do"].append(card_duel)
                        
                        game_state["boss_phase"] = f"🚫 PO REJEITOU [{card_duel['id']}]! Motivo: {reason[:40]}"
                        pixel_agents[hero_key]["action"] = f"💢 Card [{card_duel['id']}] REJEITADO! Volta ao A Fazer!"
                        
                        audit_logs.append({
                            "event_id": f"evt_{len(audit_logs)+1}",
                            "action": "PO_REJECTED",
                            "hero": hero["name"],
                            "card_id": card_duel["id"],
                            "reason": reason[:60]
                        })
                        
                        duel["is_active"] = False
                        duel["phase"] = "idle"

            await asyncio.sleep(1.0)

        if not game_state["victory"]:
            game_state["boss_phase"] = f"🔄 WAVE CONCLUÍDA! {game_state['cards_cleared_in_current_wave']}/{target_clear_count} cards. Próxima rodada..."
            await asyncio.sleep(3)


async def _do_real_commit(hero_key: str, topic: str, card_id: Optional[str] = None):
    """Sintetiza código Python REAL + Pytest e faz commit/push REAL no GitHub!"""
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

            /* DUEL ARENA */
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

            /* KANBAN */
            .kanban-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 0.4rem;
            }

            .kanban-col {
                background: rgba(0,0,0,0.5);
                border: 2px solid #30363d;
                border-radius: 6px;
                padding: 0.4rem;
                min-height: 90px;
            }

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

            /* GITHUB COMMITS */
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

            /* AUDIT LOG */
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

                <!-- DUEL BOX -->
                <div id="duel-box" class="duel-arena-box">
                    <div style="font-size:0.46rem; color:#60a5fa; text-align:center;">AGUARDANDO PROCESSO...</div>
                </div>

                <!-- KANBAN BOARD (4 COLUNAS) -->
                <div class="kanban-grid">
                    <div class="kanban-col">
                        <div class="kanban-col-title card-todo">🔴 A FAZER</div>
                        <div id="col-todo"></div>
                    </div>
                    <div class="kanban-col">
                        <div class="kanban-col-title card-progress">🔵 EM PROGRESSO</div>
                        <div id="col-progress"></div>
                    </div>
                    <div class="kanban-col">
                        <div class="kanban-col-title card-validation">🟡 EM VALIDAÇÃO</div>
                        <div id="col-validation"></div>
                    </div>
                    <div class="kanban-col">
                        <div class="kanban-col-title card-done">🟢 CONCLUÍDO</div>
                        <div id="col-done"></div>
                    </div>
                </div>

                <!-- GITHUB COMMITS REAIS -->
                <div>
                    <div style="font-size:0.44rem; color:#a855f7; margin-bottom:0.3rem;">
                        🐙 COMMITS REAIS NO GITHUB 
                        <span id="commit-count" style="color:#22c55e; font-size:0.38rem;"></span>
                    </div>
                    <div id="skills-list">Carregando heróis...</div>
                </div>

                <!-- AUDIT LOG -->
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
                // Canvas ocupa ~55% da tela
                canvas.width = Math.floor(window.innerWidth * 0.52);
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];
            let duelState = {};
            let kanbanState = {};

            // Contador global de tempo para animações
            let globalTick = 0;

            function drawPixelSprite(x, y, color, name, isDuelist, lvl, action) {
                const blink = Math.floor(Date.now() / 500) % 2 === 0;
                
                // Corpo
                ctx.fillStyle = color;
                ctx.fillRect(x, y + 10, 24, 20);

                // Cabeça
                ctx.fillStyle = "#ffcc99";
                ctx.fillRect(x + 4, y, 16, 14);

                // Olhos
                ctx.fillStyle = "#000";
                ctx.fillRect(x + 7, y + 4, 3, 3);
                ctx.fillRect(x + 14, y + 4, 3, 3);

                // Nome e nível
                ctx.font = '7px "Press Start 2P"';
                ctx.fillStyle = color;
                ctx.fillText(`${name} Lv.${lvl}`, x - 8, y - 12);

                // Ação atual (em fonte menor)
                if (action) {
                    ctx.font = '5px "Press Start 2P"';
                    ctx.fillStyle = "#9ca3af";
                    const actionText = action.substring(0, 28);
                    ctx.fillText(actionText, x - 20, y - 3);
                }

                if (isDuelist) {
                    // Efeito de brilho para o herói em duelo
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

                // Animação do boss
                const bossAnim = Math.sin(Date.now() / 400) * 3;

                // Corpo do vilão
                ctx.fillStyle = "#1e1e2e";
                ctx.fillRect(bx, by + 30 + bossAnim, 80, 70);

                // Gravata/detalhe
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 36, by + 35 + bossAnim, 8, 35);

                // Cabeça (mais ameaçadora)
                ctx.fillStyle = "#313244";
                ctx.fillRect(bx + 10, by + bossAnim, 60, 40);

                // Olhos vermelhos malignos
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 18, by + 12 + bossAnim, 14, 10);
                ctx.fillRect(bx + 48, by + 12 + bossAnim, 14, 10);

                // Chifres (vilão!)
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 15, by - 10 + bossAnim, 8, 14);
                ctx.fillRect(bx + 57, by - 10 + bossAnim, 8, 14);

                // Nome do boss
                ctx.font = '9px "Press Start 2P"';
                ctx.fillStyle = "#ff5555";
                ctx.fillText("👹 PO EVIL BOSS", bx - 30, by - 20 + bossAnim);

                // HP BAR
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

                // Fase atual (texto sob o boss)
                ctx.font = '5px "Press Start 2P"';
                ctx.fillStyle = "#ffaa00";
                const phaseShort = phaseText ? phaseText.substring(0, 55) : "";
                ctx.fillText(phaseShort, canvas.width / 2 - 160, by + 120 + bossAnim);
            }

            function render() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // Background com grid
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

                    // Mostrar fase e timer na tela
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

                    // ---- TURN BANNER ----
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

                    // ---- DUEL BOX ----
                    const duel = duelState;
                    if (duel && duel.is_active && duel.active_card) {
                        const pct = Math.max(0, (duel.timeout_timer_sec / duel.max_timeout_sec) * 100);
                        const timerColor = pct < 30 ? '#ff5555' : pct < 60 ? '#ffaa00' : '#00ff00';
                        const phaseLabel = duel.phase === "hero_working" ? `💻 HERÓI CODIFICANDO (${duel.work_progress || 0}%)` : "🔍 PO VILÃO REVISANDO";
                        const phaseColor = duel.phase === "hero_working" ? "#60a5fa" : "#ffaa00";
                        
                        document.getElementById('duel-box').innerHTML = `
                            <div style="font-size:0.52rem; color:${phaseColor}; font-weight:bold; margin-bottom:0.25rem; text-align:center;">
                                ${phaseLabel}
                            </div>
                            <div style="font-size:0.44rem; color:#3b82f6; margin-bottom:0.2rem;">
                                👔 <b>Felipe:</b> Analisou & Delegou para <span style="color:#a855f7;">${duel.active_hero}</span>!
                            </div>
                            <div style="font-size:0.46rem; color:#fff; margin-bottom:0.2rem;">
                                ⚔️ <b>Herói em Ação:</b> <span style="color:#a855f7;">${duel.active_hero}</span> — Card: <span style="color:#ec4899;">[${duel.active_card.id}]</span>
                            </div>
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

                    // ---- KANBAN (4 COLUNAS) ----
                    const activeCardId = duel && duel.active_card ? duel.active_card.id : null;
                    
                    function renderCards(cards, colorClass) {
                        return cards.map(c => {
                            const isActive = c.id === activeCardId;
                            const isRejected = c.rejections > 0;
                            return `
                                <div class="kanban-card-item ${isActive ? 'active-card' : ''} ${isRejected && !isActive ? 'rejected-card' : ''}">
                                    <div style="color:${colorClass}; font-weight:bold; font-size:0.36rem;">${c.id}</div>
                                    <div style="font-size:0.33rem; color:#d1d5db;">${(c.title || '').substring(0, 18)}...</div>
                                    ${c.rejections > 0 ? `<div style="color:#ff5555; font-size:0.3rem;">⚠️ ${c.rejections}x rejeitado</div>` : ''}
                                </div>
                            `;
                        }).join('');
                    }

                    document.getElementById('col-todo').innerHTML = renderCards(kanbanState.to_do || [], '#ff5555');
                    document.getElementById('col-progress').innerHTML = renderCards(kanbanState.in_progress || [], '#60a5fa');
                    document.getElementById('col-validation').innerHTML = renderCards(kanbanState.in_validation || [], '#ffaa00');
                    document.getElementById('col-done').innerHTML = renderCards(kanbanState.done || [], '#55ff55');

                    // ---- GITHUB COMMITS (REAIS) ----
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

                    // ---- AUDIT LOG ----
                    document.getElementById('audit-log').innerHTML = auditLogs.map(l => {
                        let cls = 'audit-log-entry';
                        if (l.action === 'PO_APPROVED') cls += ' audit-approved';
                        else if (l.action === 'PO_REJECTED') cls += ' audit-rejected';
                        else if (l.action === 'REAL_GITHUB_COMMIT') cls += ' audit-commit';
                        else if (l.action && l.action.includes('JIRA')) cls += ' audit-jira';
                        
                        const detail = l.reason || l.commit || l.card_id || l.hero || '';
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
