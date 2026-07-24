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

app = FastAPI(title="FLOSE (AEOS) - Non-Blocking Real-Time Duel Arena & Continuous Timers")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Busca os cards REAIS do Jira Cloud da sua conta (felipeflose.atlassian.net)
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=10)

game_state = {
    "boss_name": "PO EVIL BOSS",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "current_turn": "PO_BURST_PHASE", 
    "turn_timer_sec": 60,
    "boss_cards_created_in_burst": 0,
    "cards_coded_count": 0,
    "victory": False,
    "duel": {
        "is_active": False,
        "active_hero": None,
        "active_card": None,
        "timeout_timer_sec": 10.0,
        "max_timeout_sec": 10.0,
        "damage_dealt": 0
    },
    "kanban": {
        "to_do": real_jira_cards if real_jira_cards else [],
        "in_progress": [],
        "in_validation": [],
        "done": []
    }
}

pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe",
        "class": "Líder de Arquitetura",
        "sprite_color": "#3b82f6",
        "x": 100, "y": 260,
        "skill_level": 1,
        "xp": 0,
        "response_speed_ms": 450.0,
        "timeout_resistance_sec": 10.0,
        "action": "Supervisionando Duelo em Tempo Real",
    },
    "sofia": {
        "name": "Sofia",
        "class": "Gemma 4 & Ollama Analyst",
        "sprite_color": "#ec4899",
        "x": 220, "y": 220,
        "skill_level": 1,
        "xp": 0,
        "response_speed_ms": 380.0,
        "timeout_resistance_sec": 10.0,
        "action": "Minerando Soluções no Gemma 4",
    },
    "lucas": {
        "name": "Lucas",
        "class": "Claude-Code Ollama & AGY Coder",
        "sprite_color": "#f97316",
        "x": 350, "y": 270,
        "skill_level": 1,
        "xp": 0,
        "response_speed_ms": 250.0,
        "timeout_resistance_sec": 10.0,
        "action": "Codificando sem Bloquear o Cronômetro",
    },
    "beatriz": {
        "name": "Beatriz",
        "class": "QA & Security Shield",
        "sprite_color": "#10b981",
        "x": 480, "y": 230,
        "skill_level": 1,
        "xp": 0,
        "response_speed_ms": 400.0,
        "timeout_resistance_sec": 10.0,
        "action": "Auditando Testes de Timeout",
    }
}

audit_logs: List[Dict[str, Any]] = []

def check_autonomous_skill_evolution(agent_key: str):
    agt = pixel_agents[agent_key]
    agt["xp"] += 35
    if agt["xp"] >= 100:
        agt["xp"] = 0
        agt["skill_level"] += 1
        agt["response_speed_ms"] = max(30.0, round(agt["response_speed_ms"] * 0.75, 1))
        agt["timeout_resistance_sec"] += 2.0
        
        audit_logs.append({
            "event_id": f"evt_{len(audit_logs)+1}",
            "action": "HERO_SKILL_LEVEL_UP",
            "agent": agt["name"],
            "new_level": agt["skill_level"],
            "speed": f"{agt['response_speed_ms']}ms"
        })

# TASK ASSÍNCRONA EM SEGUNDO PLANO PARA CRIAÇÃO DE CARDS NO JIRA SEM BLOQUEAR O CRONÔMETRO
async def async_create_jira_card_background(topic_title: str, topic_desc: str):
    try:
        jira_res = await asyncio.to_thread(jira.create_detailed_epic_or_task, "KAN", topic_title, topic_desc, "ÉPICO PO GEMMA4")
        new_key = jira_res.get("key", f"KAN-{random.randint(9700, 9999)}")
        new_card = {
            "id": new_key,
            "title": f"[PO-GEMMA4] {topic_title}",
            "description": topic_desc,
            "status": "A FAZER",
            "rejections": 0,
            "comments": [{"author": "PO EVIL BOSS", "text": f"Criado com Gemma 4 no 'A FAZER': {topic_title}."}]
        }
        game_state["kanban"]["to_do"].append(new_card)
        game_state["boss_cards_created_in_burst"] += 1
        game_state["boss_phase"] = f"🔥 PO CREATED CARD REAL {new_key} NO JIRA!"
        
        audit_logs.append({
            "event_id": f"evt_{len(audit_logs)+1}",
            "action": "PO_REAL_JIRA_CARD_CREATED",
            "card_id": new_key,
            "title": topic_title
        })
    except Exception as e:
        print(f"[Async Jira Error] {e}")

# LOOP PRINCIPAL TOTALMENTE NÃO-BLOQUEANTE (O CRONÔMETRO NUNCA PARA!)
async def non_blocking_continuous_game_loop():
    po_turn_duration = 60      # 1 Minuto para o PO
    heroes_turn_duration = 120 # 2 Minutos para os Heróis
    
    while True:
        # =========================================================================
        # FASE 1: TURNO DO PO VILÃO (60 SEGUNDOS - CRONÔMETRO 100% CONTÍNUO)
        # =========================================================================
        game_state["current_turn"] = "PO_BURST_PHASE"
        game_state["boss_cards_created_in_burst"] = 0
        game_state["duel"]["is_active"] = False

        for sec in range(po_turn_duration, 0, -1):
            if game_state["victory"]: break
            game_state["turn_timer_sec"] = sec

            # Dispara chamadas de rede no background sem travar o loop de 1 segundo!
            if game_state["boss_cards_created_in_burst"] < 5 and sec % 10 == 0:
                po_topics = [
                    ("Refatorar UI Frontend Nível Pixel Perfect 16-Bit", "O PO Vilão exige alinhamento perfeito de bordas HSL."),
                    ("Otimização de Performance Backend Async & Caching", "Cobrança do PO: Reduzir a latência do EventBus para <5ms."),
                    ("Auditoria Anti-Alucinação e Cobertura de Testes Mutation", "Exigência do PO: Adicionar testes de mutação com evidência SHA-256."),
                    ("CONTRATAÇÃO: Onboarding de Desenvolvedor Frontend Senior", "Demanda de RH do PO: Recrutar colaborador especialista em React."),
                    ("Sanitização Estrita contra Vulnerabilidades XSS & SQL", "O PO encontrou potenciais falhas nos endpoints REST.")
                ]
                topic_title, topic_desc = po_topics[game_state["boss_cards_created_in_burst"] % len(po_topics)]
                asyncio.create_task(async_create_jira_card_background(topic_title, topic_desc))

            # CRONÔMETRO EXATO DE 1.0 SEGUNDO SEM BLOQUEIOS
            await asyncio.sleep(1.0)

        # =========================================================================
        # FASE 2: TURNO DOS HERÓIS (120 SEGUNDOS - CRONÔMETRO 100% CONTÍNUO E ININTERRUPTO)
        # =========================================================================
        game_state["current_turn"] = "HEROES_REST_PHASE"
        game_state["boss_phase"] = "⚔️ ARENA DE DUELO: CRONÔMETRO CONTÍNUO EM TEMPO REAL!"

        for sec in range(heroes_turn_duration, 0, -1):
            if game_state["victory"]: break
            game_state["turn_timer_sec"] = sec  # O CRONÔMETRO DECREMENTA SEM NENHUMA PAUSA!

            # 1. Se não há duelo ativo, inicia imediatamente com o próximo card!
            if not game_state["duel"]["is_active"] and game_state["kanban"]["to_do"]:
                card = game_state["kanban"]["to_do"].pop(0)
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

                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "DUEL_STARTED",
                    "hero": hero["name"],
                    "card_id": card["id"]
                })

            # 2. Se há duelo ativo, atualiza a contagem regressiva do timeout do duelo sem travar o relógio principal!
            if game_state["duel"]["is_active"]:
                duel = game_state["duel"]
                hero_key = duel["hero_key"]
                hero = pixel_agents[hero_key]

                duel["timeout_timer_sec"] = round(duel["timeout_timer_sec"] - 1.0, 1)

                # Herói vence o duelo se responder rápido!
                if duel["timeout_timer_sec"] > 0 and random.random() < (0.35 + (hero["skill_level"] * 0.1)):
                    card_duel = duel["active_card"]
                    check_autonomous_skill_evolution(hero_key)

                    card_duel["status"] = "CONCLUÍDO"
                    damage = 250
                    game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                    
                    if card_duel in game_state["kanban"]["in_progress"]:
                        game_state["kanban"]["in_progress"].remove(card_duel)
                    game_state["kanban"]["done"].append(card_duel)
                    game_state["cards_coded_count"] += 1

                    game_state["boss_phase"] = f"💥 {hero['name']} VENCEU O DUELO NO CARD {card_duel['id']}! (-250 HP)"
                    
                    h = governance.generate_audit_hash("agt_lucas", "NON_BLOCKING_DUEL_WON", card_duel['title'])
                    audit_logs.append({
                        "event_id": f"evt_{len(audit_logs)+1}",
                        "action": "DUEL_WON_BEFORE_TIMEOUT",
                        "hero": hero["name"],
                        "card_id": card_duel["id"],
                        "hash": h
                    })

                    duel["is_active"] = False

                    if game_state["boss_hp"] <= 0:
                        game_state["victory"] = True
                        game_state["boss_phase"] = "🏆 VITÓRIA! OS HERÓIS VENCERAM TODOS OS DUELOS E DERROTARAM O PO VILÃO!"

                elif duel["timeout_timer_sec"] <= 0:
                    # TIMEOUT REAL!
                    card_duel = duel["active_card"]
                    card_duel["rejections"] += 1
                    card_duel["status"] = "A FAZER"
                    
                    if card_duel in game_state["kanban"]["in_progress"]:
                        game_state["kanban"]["in_progress"].remove(card_duel)
                    game_state["kanban"]["to_do"].append(card_duel)

                    game_state["boss_phase"] = f"💥 TIMEOUT STRIKE! {hero['name']} DEMOROU DEMAIS NO CARD {card_duel['id']}!"

                    audit_logs.append({
                        "event_id": f"evt_{len(audit_logs)+1}",
                        "action": "REAL_TIMEOUT_STRIKE",
                        "hero": hero["name"],
                        "card_id": card_duel["id"]
                    })

                    duel["is_active"] = False

            # DORMIDA EXATA DE 1 SEGUNDO (CRONÔMETRO NUNCA MAIS TRAVA!)
            await asyncio.sleep(1.0)

@app.on_event("startup")
async def start_autonomous_loop():
    await bus.start()
    asyncio.create_task(non_blocking_continuous_game_loop())

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
        <title>FLOSE AEOS - Non-Blocking Real-Time Duel Arena & Continuous Timers</title>
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
                background: rgba(236, 72, 153, 0.2);
                border: 2px solid #ec4899;
                border-radius: 6px;
                padding: 0.6rem;
                text-align: center;
                margin-bottom: 1rem;
                font-size: 0.52rem;
            }

            .duel-arena-box {
                background: rgba(236, 72, 153, 0.15);
                border: 2px solid #ec4899;
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
                    <div class="hud-title">⚡ CRONÔMETRO CONTÍNUO & DUELO DE TIMEOUT</div>
                    
                    <div id="turn-banner" class="turn-banner">
                        TURNO ATUAL: CARREGANDO...
                    </div>

                    <!-- CAIXA DE DUELO EM TEMPO REAL -->
                    <div id="duel-box" class="duel-arena-box">
                        <div style="font-size:0.5rem; color:#ec4899; text-align:center;">AGUARDANDO DUELO...</div>
                    </div>

                    <!-- QUADRO KANBAN EM TEMPO REAL -->
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

                    <div style="font-size:0.48rem; color:#a855f7; margin-bottom:0.4rem;">🛡️ EVOLUÇÃO AUTÔNOMA DOS DUELISTAS:</div>
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
                    ctx.fillStyle = "#ffaa00";
                    ctx.fillRect(x - 2, y - 22, 28, 8);
                    ctx.font = '5px "Press Start 2P"';
                    ctx.fillStyle = "#000";
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
                ctx.fillText("👹 PO EVIL BOSS", bx - 30, by - 15);

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
                    drawPOBoss(hpPct, gameState.boss_phase || "Cronômetro Contínuo...");

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

                // Turn Banner Display
                const isPoTurn = gameState.current_turn === "PO_BURST_PHASE";
                document.getElementById('turn-banner').style.borderColor = isPoTurn ? "#ff5555" : "#55ff55";
                document.getElementById('turn-banner').style.color = isPoTurn ? "#ff5555" : "#55ff55";
                document.getElementById('turn-banner').innerHTML = isPoTurn ?
                    `👹 TURNO PO: GEMMA 4 (5 CARDS JIRA) | ⏱️ ${gameState.turn_timer_sec}s` :
                    `⚡ TURNO HERÓIS: CLAUDE-CODE & EVOLUÇÃO SKILL | ⏱️ ${gameState.turn_timer_sec}s`;

                // Render Caixa de Duelo em Tempo Real
                if (duel && duel.is_active && duel.active_card) {
                    const pct = Math.max(0, (duel.timeout_timer_sec / duel.max_timeout_sec) * 100);
                    document.getElementById('duel-box').innerHTML = `
                        <div style="font-size:0.55rem; color:#f59e0b; font-weight:bold; margin-bottom:0.4rem;">
                            ⚔️ DUELO EM ANDAMENTO: <span style="color:#60a5fa;">${duel.active_hero}</span> VS PO!
                        </div>
                        <div style="font-size:0.48rem; color:#ec4899; margin-bottom:0.4rem;">
                            🎴 CARD EM CODIFICAÇÃO: [${duel.active_card.id}] ${duel.active_card.title}
                        </div>
                        <div style="font-size:0.45rem; color:#9ca3af;">
                            ⏱️ CRONÔMETRO DE TIMEOUT REAL: <span style="color:${pct < 40 ? '#ff5555' : '#00ff00'}; font-weight:bold;">${duel.timeout_timer_sec.toFixed(1)}s</span>
                        </div>
                        <div class="duel-timer-bg">
                            <div class="duel-timer-fill" style="width:${pct}%; background:${pct < 40 ? '#ff5555' : '#00ff00'};"></div>
                        </div>
                    `;
                } else {
                    document.getElementById('duel-box').innerHTML = `
                        <div style="font-size:0.48rem; color:#9ca3af; text-align:center;">
                            😴 NENHUM DUELO ATIVO NO MOMENTO. O PO ESTÁ GERANDO CARDS NO 'A FAZER'...
                        </div>
                    `;
                }

                // Render Kanban
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

                // Render Lista de Heróis
                document.getElementById('skills-list').innerHTML = agentsList.map(a => `
                    <div style="background:rgba(0,0,0,0.5); border:1px solid #30363d; padding:0.4rem; border-radius:4px; margin-bottom:0.3rem; font-size:0.42rem;">
                        <div style="color:${a.sprite_color}; font-weight:bold;">${a.name} (Lv.${a.skill_level}) <span style="float:right; color:#a855f7;">XP: ${a.xp}%</span></div>
                        <div style="color:#9ca3af; margin-top:0.2rem;">Velocidade: <span style="color:#55ffff;">${a.response_speed_ms.toFixed(0)}ms</span> | Resistência Timeout: ${a.timeout_resistance_sec.toFixed(1)}s</div>
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
