import asyncio
import time
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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

app = FastAPI(title="FLOSE (AEOS) - Dynamic PO Frenzy & Hero Training Ground")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Busca os cards REAIS do Jira Cloud da sua conta (felipeflose.atlassian.net)
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=10)
for c in real_jira_cards:
    c.setdefault("rejections", 0)

game_state = {
    "boss_name": "PO EVIL BOSS (FRENZY MODE)",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "current_phase": "HERO_TRAINING_PHASE", # HERO_TRAINING_PHASE (2 min vantagem) -> PO_FRENZY_30S -> HEROES_CLEARING_PHASE (limpar 80%)
    "phase_timer_sec": 120,
    "boss_cards_created_in_frenzy": 0,
    "target_cards_to_clear_80pct": 0,
    "cards_cleared_in_current_wave": 0,
    "cards_coded_count": 0,
    "victory": False,
    "duel": {
        "is_active": False,
        "active_hero": None,
        "active_card": None,
        "timeout_timer_sec": 18.0,
        "max_timeout_sec": 18.0,
        "damage_dealt": 0
    },
    "kanban": {
        "to_do": real_jira_cards if real_jira_cards else [],
        "in_progress": [],
        "in_validation": [],
        "done": []
    }
}

# HERÓIS COM ACADEMIA DE TREINAMENTO E APRENDIZADO DE NOVAS SKILLS
pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe",
        "class": "Líder de Arquitetura",
        "sprite_color": "#3b82f6",
        "x": 100, "y": 260,
        "skill_level": 1,
        "xp": 0,
        "new_skills_learned": ["Arquitetura Async Core", "Gerenciamento de Memória"],
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
        "new_skills_learned": ["Fine-Tuning Gemma 4", "Prompt Optimization"],
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
        "new_skills_learned": ["Refatoração Rust/Python", "AGY Automation"],
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
        "new_skills_learned": ["Testes de Mutação", "Zero-Trust Security"],
        "response_speed_ms": 210.0,
        "timeout_resistance_sec": 18.0,
        "action": "Aprimorando Suíte de Testes de Aceite",
    }
}

audit_logs: List[Dict[str, Any]] = []

def learn_new_skills_autonomously(agent_key: str):
    agt = pixel_agents[agent_key]
    agt["xp"] += 50
    skills_pool = ["Design Pattern Master", "EventBus Acceleration", "Ollama Quantization", "AGY Scripting", "Pixel Perfect CSS Engine"]
    new_skill = random.choice(skills_pool)
    if new_skill not in agt["new_skills_learned"]:
        agt["new_skills_learned"].append(new_skill)
    
    if agt["xp"] >= 100:
        agt["xp"] = 0
        agt["skill_level"] += 1
        agt["response_speed_ms"] = max(15.0, round(agt["response_speed_ms"] * 0.65, 1))
        agt["timeout_resistance_sec"] += 3.0
        
        audit_logs.append({
            "event_id": f"evt_{len(audit_logs)+1}",
            "action": "HERO_LEARNED_NEW_SKILL",
            "agent": agt["name"],
            "new_skill": new_skill,
            "new_level": agt["skill_level"]
        })

async def async_create_jira_card_background(topic_title: str, topic_desc: str):
    try:
        jira_res = await asyncio.to_thread(jira.create_detailed_epic_or_task, "KAN", topic_title, topic_desc, "ÉPICO PO FRENZY")
        new_key = jira_res.get("key", f"KAN-{random.randint(9700, 9999)}")
        new_card = {
            "id": new_key,
            "title": f"[PO-FRENZY] {topic_title}",
            "description": topic_desc,
            "status": "A FAZER",
            "rejections": 0,
            "comments": [{"author": "PO EVIL BOSS", "text": f"Criado na Rajada de 30s: {topic_title}."}]
        }
        game_state["kanban"]["to_do"].append(new_card)
        game_state["boss_cards_created_in_frenzy"] += 1
        
        audit_logs.append({
            "event_id": f"evt_{len(audit_logs)+1}",
            "action": "PO_FRENZY_CARD_CREATED",
            "card_id": new_key,
            "title": topic_title
        })
    except Exception as e:
        print(f"[Async Jira Error] {e}")

# NOVO CICLO DINÂMICO DE REGRAS SOLICITADO:
# 1. HERÓIS GANHAM 2 MINUTOS DE VANTAGEM INICIAL PARA ESTUDAR E APRENDER NOVAS SKILLS!
# 2. PO ENTRA EM MODO FRENZY DE 30 SEGUNDOS E CRIA O MÁXIMO DE CARDS QUE CONSEGUIR NO JIRA!
# 3. OS HERÓIS ENTRAM EM AÇÃO E SÓ VOLTAM AO TURNO NORMAL APÓS LIMPAR 80% DOS CARDS CRIADOS!
async def dynamic_frenzy_and_training_game_loop():
    while True:
        # =========================================================================
        # REGRA 1: FASE DE TREINAMENTO DOS HERÓIS (2 MINUTOS / 120 SEGUNDOS DE VANTAGEM)
        # =========================================================================
        game_state["current_phase"] = "HERO_TRAINING_PHASE"
        game_state["boss_phase"] = "🎓 ACADEMIA DOS HERÓIS: 2 MINUTOS DE VANTAGEM PARA ESTUDAR E EVOLUIR SKILLS!"
        game_state["duel"]["is_active"] = False

        for sec in range(120, 0, -1):
            if game_state["victory"]: break
            game_state["phase_timer_sec"] = sec

            # Todos os heróis aprendem novas skills continuamente durante o treinamento!
            if sec % 5 == 0:
                hero_k = random.choice(["felipe", "sofia", "lucas", "beatriz"])
                learn_new_skills_autonomously(hero_k)
                pixel_agents[hero_k]["action"] = f"🎓 Aprendendo nova skill: {pixel_agents[hero_k]['new_skills_learned'][-1]}"

            await asyncio.sleep(1.0)

        # =========================================================================
        # REGRA 2: PO ENTRA EM JANELA FRENZY DE 30 SEGUNDOS (GERA TUDO QUE CONSEGUIR!)
        # =========================================================================
        game_state["current_phase"] = "PO_FRENZY_30S"
        game_state["boss_phase"] = "⚡ PO FRENZY MODE! 30 SEGUNDOS GERANDO O MÁXIMO DE CARDS NO JIRA!"
        game_state["boss_cards_created_in_frenzy"] = 0

        po_topics_frenzy = [
            ("Refatorar UI Frontend Nível Pixel Perfect 16-Bit", "PO exige alinhamento HSL."),
            ("Otimização de Performance Backend Async & Caching", "Latência do EventBus <5ms."),
            ("Auditoria Anti-Alucinação e Cobertura de Testes Mutation", "Testes de mutação com evidência SHA-256."),
            ("CONTRATAÇÃO: Onboarding de Desenvolvedor Frontend Senior", "Recrutar colaborador especialista em React."),
            ("Sanitização Estrita contra Vulnerabilidades XSS & SQL", "Falhas de segurança nos endpoints REST."),
            ("Implementação de Protocolo MCP Bridge", "Exportar métricas de telemetria."),
            ("Melhoria de Cores e Gradientes em 2D/3D Canvas", "Bordas dinâmicas e animações smooth.")
        ]

        for sec in range(30, 0, -1):
            if game_state["victory"]: break
            game_state["phase_timer_sec"] = sec

            # Dispara requisições contínuas a cada 2 segundos na janela de 30s!
            if sec % 2 == 0:
                topic_title, topic_desc = po_topics_frenzy[game_state["boss_cards_created_in_frenzy"] % len(po_topics_frenzy)]
                asyncio.create_task(async_create_jira_card_background(topic_title, topic_desc))

            await asyncio.sleep(1.0)

        # =========================================================================
        # REGRA 3: HERÓIS PRECISAM RESOLVER E BAIXAR PELO MENOS 80% DOS CARDS CRIADOS!
        # =========================================================================
        cards_created = max(1, game_state["boss_cards_created_in_frenzy"])
        target_clear_count = int(cards_created * 0.8) # 80% dos cards criados!
        game_state["target_cards_to_clear_80pct"] = target_clear_count
        game_state["cards_cleared_in_current_wave"] = 0
        game_state["current_phase"] = "HEROES_CLEARING_PHASE"

        game_state["boss_phase"] = f"⚔️ META DOS HERÓIS: BAIXAR 80% DOS CARDS ({target_clear_count} CARDS) DA RAJADA!"

        while game_state["cards_cleared_in_current_wave"] < target_clear_count:
            if game_state["victory"]: break

            # Se não há duelo ativo, inicia duelo no card
            if not game_state["duel"]["is_active"] and game_state["kanban"]["to_do"]:
                card = game_state["kanban"]["to_do"].pop(0)
                card.setdefault("rejections", 0)
                card["status"] = "EM PROGRESSO"
                game_state["kanban"]["in_progress"].append(card)

                hero_key = random.choice(["felipe", "sofia", "lucas", "beatriz"])
                hero = pixel_agents[hero_key]

                game_state["duel"] = {
                    "is_active": True,
                    "active_hero": hero["name"],
                    "hero_key": hero_key,
                    "active_card": card,
                    "timeout_timer_sec": hero["timeout_resistance_sec"],
                    "max_timeout_sec": hero["timeout_resistance_sec"],
                    "damage_dealt": 0
                }

            # Executa o duelo com as novas habilidades aprendidas pelos heróis!
            if game_state["duel"]["is_active"]:
                duel = game_state["duel"]
                hero_key = duel["hero_key"]
                hero = pixel_agents[hero_key]

                duel["timeout_timer_sec"] = round(duel["timeout_timer_sec"] - 1.0, 1)

                # Heróis agora estão MUITO MAIS ESPERTOS (85% de acerto com as novas skills aprendidas!)
                if duel["timeout_timer_sec"] > 0 and random.random() < (0.75 + (hero["skill_level"] * 0.05)):
                    card_duel = duel["active_card"]
                    
                    card_duel["status"] = "CONCLUÍDO"
                    damage = 300
                    game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                    
                    if card_duel in game_state["kanban"]["in_progress"]:
                        game_state["kanban"]["in_progress"].remove(card_duel)
                    game_state["kanban"]["done"].append(card_duel)
                    game_state["cards_coded_count"] += 1
                    game_state["cards_cleared_in_current_wave"] += 1

                    game_state["boss_phase"] = f"💥 {hero['name']} RESPEITOU A META! ({game_state['cards_cleared_in_current_wave']}/{target_clear_count} CARDS 80%)"
                    
                    h = governance.generate_audit_hash("agt_lucas", "HERO_80PCT_CLEAR_CARD", card_duel['title'])
                    audit_logs.append({
                        "event_id": f"evt_{len(audit_logs)+1}",
                        "action": "HERO_80PCT_CARD_RESOLVED",
                        "hero": hero["name"],
                        "card_id": card_duel["id"],
                        "hash": h
                    })

                    duel["is_active"] = False

                    if game_state["boss_hp"] <= 0:
                        game_state["victory"] = True
                        game_state["boss_phase"] = "🏆 VITÓRIA ABSOLUTA! OS HERÓIS BAIXARAM 80% DOS CARDS E DERROTARAM O PO VILÃO!"

                elif duel["timeout_timer_sec"] <= 0:
                    card_duel = duel["active_card"]
                    card_duel.setdefault("rejections", 0)
                    card_duel["rejections"] += 1
                    card_duel["status"] = "A FAZER"
                    
                    if card_duel in game_state["kanban"]["in_progress"]:
                        game_state["kanban"]["in_progress"].remove(card_duel)
                    game_state["kanban"]["to_do"].append(card_duel)

                    duel["is_active"] = False

            await asyncio.sleep(1.0)

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
        "audit_logs": audit_logs[-6:],
    }

@app.get("/", response_class=HTMLResponse)
async def serve_autonomous_pixel_game():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE AEOS - Dynamic PO Frenzy & Hero Training Ground</title>
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
            }

            .side-panel {
                width: 560px;
                background: #11121d;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border-left: 4px solid #3b3d54;
                overflow-y: auto;
            }

            .hud-title {
                font-size: 0.65rem;
                color: #55ff55;
                margin-bottom: 0.8rem;
                text-shadow: 2px 2px #00aa00;
            }

            .turn-banner {
                background: rgba(168, 85, 247, 0.2);
                border: 2px solid #a855f7;
                border-radius: 6px;
                padding: 0.6rem;
                text-align: center;
                margin-bottom: 1rem;
                font-size: 0.52rem;
            }

            .duel-arena-box {
                background: rgba(59, 130, 246, 0.15);
                border: 2px solid #3b82f6;
                border-radius: 8px;
                padding: 0.8rem;
                margin-bottom: 1rem;
            }

            .duel-timer-bg {
                width: 100%;
                height: 14px;
                background: #440000;
                border: 2px solid #ff5555;
                border-radius: 4px;
                margin-top: 0.5rem;
                overflow: hidden;
            }

            .duel-timer-fill {
                height: 100%;
                background: #00ff00;
                transition: width 0.3s linear;
            }

            .kanban-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.5rem;
                margin-bottom: 1rem;
            }

            .kanban-col {
                background: rgba(0,0,0,0.5);
                border: 2px solid #30363d;
                border-radius: 6px;
                padding: 0.5rem;
                min-height: 100px;
            }

            .kanban-col-title {
                font-size: 0.4rem;
                font-weight: bold;
                margin-bottom: 0.4rem;
                text-align: center;
            }

            .card-todo { color: #ff5555; }
            .card-validation { color: #ffaa00; }
            .card-done { color: #55ff55; }

            .kanban-card-item {
                background: rgba(255,255,255,0.05);
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 0.4rem;
                margin-bottom: 0.4rem;
                font-size: 0.38rem;
                line-height: 1.3;
            }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>

            <div class="side-panel">
                <div>
                    <div class="hud-title">⚡ PO FRENZY 30s & ACADEMIA DOS HERÓIS</div>
                    
                    <div id="turn-banner" class="turn-banner">
                        FASE ATUAL: CARREGANDO...
                    </div>

                    <!-- CAIXA DE DUELO COM SKILLS APRENDIDAS -->
                    <div id="duel-box" class="duel-arena-box">
                        <div style="font-size:0.5rem; color:#60a5fa; text-align:center;">AGUARDANDO PROCESSO...</div>
                    </div>

                    <div class="kanban-grid">
                        <div class="kanban-col">
                            <div class="kanban-col-title card-todo">🔴 A FAZER</div>
                            <div id="col-todo"></div>
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

                    <div style="font-size:0.48rem; color:#a855f7; margin-bottom:0.4rem;">🎓 NOVAS SKILLS APRENDIDAS PELOS HERÓIS:</div>
                    <div id="skills-list">Carregando heróis...</div>
                </div>

                <div>
                    <div style="font-size: 0.45rem; color: #55ff55; margin-bottom: 0.3rem;">📜 AUDIT LOG JIRA REAL</div>
                    <div id="audit-log" style="font-size: 0.4rem; color: #9ca3af; max-height: 70px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('pixel-canvas');
            const ctx = canvas.getContext('2d');

            function resizeCanvas() {
                canvas.width = window.innerWidth - 560;
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];

            function drawPixelSprite(x, y, color, name, isDuelist, lvl) {
                ctx.fillStyle = color;
                ctx.fillRect(x, y + 10, 24, 20);

                ctx.fillStyle = "#ffcc99";
                ctx.fillRect(x + 4, y, 16, 14);

                ctx.fillStyle = "#000";
                ctx.fillRect(x + 7, y + 4, 3, 3);
                ctx.fillRect(x + 14, y + 4, 3, 3);

                ctx.font = '7px "Press Start 2P"';
                ctx.fillStyle = color;
                ctx.fillText(`${name} (Lv.${lvl})`, x - 10, y - 10);

                if (isDuelist) {
                    ctx.fillStyle = "#3b82f6";
                    ctx.fillRect(x - 2, y - 22, 28, 8);
                    ctx.font = '5px "Press Start 2P"';
                    ctx.fillStyle = "#fff";
                    ctx.fillText("⚔️ DUELO", x, y - 16);
                }
            }

            function drawPOBoss(hpPercent, phaseText) {
                const bx = canvas.width / 2 - 40;
                const by = 40;

                ctx.fillStyle = "#1e1e2e";
                ctx.fillRect(bx, by + 30, 80, 70);

                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 36, by + 35, 8, 35);

                ctx.fillStyle = "#313244";
                ctx.fillRect(bx + 10, by, 60, 40);

                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 20, by + 12, 12, 8);
                ctx.fillRect(bx + 48, by + 12, 12, 8);

                ctx.font = '10px "Press Start 2P"';
                ctx.fillStyle = "#ff5555";
                ctx.fillText("👹 PO FRENZY BOSS", bx - 40, by - 15);

                ctx.fillStyle = "#440000";
                ctx.fillRect(canvas.width / 2 - 150, 15, 300, 16);
                ctx.fillStyle = "#ff3333";
                ctx.fillRect(canvas.width / 2 - 150, 15, (300 * hpPercent) / 100, 16);
                ctx.strokeStyle = "#ffffff";
                ctx.strokeRect(canvas.width / 2 - 150, 15, 300, 16);

                ctx.font = '6px "Press Start 2P"';
                ctx.fillStyle = "#ffaa00";
                ctx.fillText(phaseText.substring(0, 50), canvas.width / 2 - 140, 42);
            }

            function render() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#11111b";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                for (let i = 0; i < canvas.width; i += 40) {
                    ctx.strokeStyle = "#1e1e2e";
                    ctx.beginPath();
                    ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height);
                    ctx.stroke();
                }

                if (gameState) {
                    const hpPct = (gameState.boss_hp / gameState.boss_max_hp) * 100;
                    drawPOBoss(hpPct, gameState.boss_phase || "Carregando...");

                    const duel = gameState.duel;
                    agentsList.forEach(a => {
                        const isDuelist = duel && duel.is_active && duel.active_hero === a.name;
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, isDuelist, a.skill_level);
                    });
                }

                requestAnimationFrame(render);
            }
            render();

            async function updateState() {
                const res = await fetch('/api/boss/state');
                const data = await res.json();
                gameState = data.game_state;
                agentsList = data.pixel_agents;
                const duel = data.duel;
                const kanban = data.kanban;

                // Dynamic Turn Banner
                const phase = gameState.current_phase;
                if (phase === "HERO_TRAINING_PHASE") {
                    document.getElementById('turn-banner').style.borderColor = "#a855f7";
                    document.getElementById('turn-banner').style.color = "#a855f7";
                    document.getElementById('turn-banner').innerHTML = `🎓 ACADEMIA: 2 MINUTOS DE ESTUDO & SKILLS | ⏱️ ${gameState.phase_timer_sec}s`;
                } else if (phase === "PO_FRENZY_30S") {
                    document.getElementById('turn-banner').style.borderColor = "#ff5555";
                    document.getElementById('turn-banner').style.color = "#ff5555";
                    document.getElementById('turn-banner').innerHTML = `🔥 PO FRENZY MODE: 30 SEGUNDOS GERANDO CARDS | ⏱️ ${gameState.phase_timer_sec}s`;
                } else {
                    document.getElementById('turn-banner').style.borderColor = "#55ff55";
                    document.getElementById('turn-banner').style.color = "#55ff55";
                    document.getElementById('turn-banner').innerHTML = `⚔️ HERÓIS LIMPANDO METAS (80% DOS CARDS): ${gameState.cards_cleared_in_current_wave}/${gameState.target_cards_to_clear_80pct}`;
                }

                if (duel && duel.is_active && duel.active_card) {
                    const pct = Math.max(0, (duel.timeout_timer_sec / duel.max_timeout_sec) * 100);
                    document.getElementById('duel-box').innerHTML = `
                        <div style="font-size:0.55rem; color:#60a5fa; font-weight:bold; margin-bottom:0.4rem;">
                            ⚔️ DUELO EM ANDAMENTO: <span style="color:#a855f7;">${duel.active_hero}</span> VS PO!
                        </div>
                        <div style="font-size:0.48rem; color:#ec4899; margin-bottom:0.4rem;">
                            🎴 CARD EM CODIFICAÇÃO: [${duel.active_card.id}] ${duel.active_card.title}
                        </div>
                        <div style="font-size:0.45rem; color:#9ca3af;">
                            ⏱️ TIMEOUT: <span style="color:${pct < 30 ? '#ff5555' : '#00ff00'}; font-weight:bold;">${duel.timeout_timer_sec.toFixed(1)}s</span>
                        </div>
                        <div class="duel-timer-bg">
                            <div class="duel-timer-fill" style="width:${pct}%; background:${pct < 30 ? '#ff5555' : '#00ff00'};"></div>
                        </div>
                    `;
                } else {
                    document.getElementById('duel-box').innerHTML = `
                        <div style="font-size:0.48rem; color:#9ca3af; text-align:center;">
                            ${phase === "HERO_TRAINING_PHASE" ? "🎓 HERÓIS NO CENTRO DE TREINAMENTO APRENDENDO NOVAS SKILLS!" : "😴 AGUARDANDO PRÓXIMO CARD DA META..."}
                        </div>
                    `;
                }

                document.getElementById('col-todo').innerHTML = kanban.to_do.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#ff5555; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 15)}...</div>
                    </div>
                `).join('');

                document.getElementById('col-validation').innerHTML = kanban.in_validation.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#ffaa00; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 15)}...</div>
                    </div>
                `).join('');

                document.getElementById('col-done').innerHTML = kanban.done.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#55ff55; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 15)}...</div>
                    </div>
                `).join('');

                // Render Novas Skills Aprendidas
                document.getElementById('skills-list').innerHTML = agentsList.map(a => `
                    <div style="background:rgba(0,0,0,0.5); border:1px solid #30363d; padding:0.4rem; border-radius:4px; margin-bottom:0.3rem; font-size:0.41rem;">
                        <div style="color:${a.sprite_color}; font-weight:bold;">${a.name} (Lv.${a.skill_level}) <span style="float:right; color:#a855f7;">XP: ${a.xp}%</span></div>
                        <div style="color:#55ff55; margin-top:0.2rem;">Skills Aprendidas: ${a.new_skills_learned.join(', ')}</div>
                    </div>
                `).join('');

                document.getElementById('audit-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.2rem;">> ${l.action}: ${l.hero || l.card_id || ''}</div>
                `).join('');
            }

            updateState();
            setInterval(updateState, 400);
        </script>
    </body>
    </html>
    """
