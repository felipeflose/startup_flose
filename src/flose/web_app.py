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

app = FastAPI(title="FLOSE (AEOS) - Real-Time Kanban & Autonomous Skill Evolution")

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
    "current_working_card": None,
    "kanban": {
        "to_do": real_jira_cards if real_jira_cards else [],
        "in_progress": [],
        "in_validation": [],
        "done": []
    }
}

# HERÓIS COM EVOLUÇÃO AUTÔNOMA DE SKILL E GAUGE DE VIDA/TIMEOUT!
pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe",
        "class": "Líder de Arquitetura",
        "sprite_color": "#3b82f6",
        "x": 100, "y": 260,
        "skill_level": 1,
        "xp": 0,
        "response_time_ms": 500.0,    # Tempo de resposta (ms) que diminui com evolução!
        "time_remaining_sec": 12.0,   # BARRA DE VIDA = TEMPO ANTES DO TIMEOUT
        "max_time_sec": 12.0,
        "can_use_gemma": False,
        "action": "Evoluindo Skill Autonomamente",
    },
    "sofia": {
        "name": "Sofia",
        "class": "Gemma 4 & Ollama Analyst",
        "sprite_color": "#ec4899",
        "x": 220, "y": 220,
        "skill_level": 1,
        "xp": 0,
        "response_time_ms": 420.0,
        "time_remaining_sec": 12.0,
        "max_time_sec": 12.0,
        "can_use_gemma": False,
        "action": "Aprendendo Padrões de Código no Gemma 4",
    },
    "lucas": {
        "name": "Lucas",
        "class": "Claude-Code Ollama & AGY Coder",
        "sprite_color": "#f97316",
        "x": 350, "y": 270,
        "skill_level": 1,
        "xp": 0,
        "response_time_ms": 300.0,
        "time_remaining_sec": 12.0,
        "max_time_sec": 12.0,
        "can_use_gemma": False,
        "action": "Codificando e Otimizando Latência",
    },
    "beatriz": {
        "name": "Beatriz",
        "class": "QA & Security Shield",
        "sprite_color": "#10b981",
        "x": 480, "y": 230,
        "skill_level": 1,
        "xp": 0,
        "response_time_ms": 450.0,
        "time_remaining_sec": 12.0,
        "max_time_sec": 12.0,
        "can_use_gemma": False,
        "action": "Auditando Testes antes do Timeout",
    }
}

audit_logs: List[Dict[str, Any]] = []

def check_autonomous_skill_evolution(agent_key: str):
    """Evolui autonomamente a skill do agente quando atinge XP suficiente!"""
    agt = pixel_agents[agent_key]
    agt["xp"] += 35
    if agt["xp"] >= 100:
        agt["xp"] = 0
        agt["skill_level"] += 1
        # Diminui o tempo de resposta (fica mais rápido) e aumenta a resistência a Timeout!
        agt["response_time_ms"] = max(30.0, round(agt["response_time_ms"] * 0.75, 1))
        agt["max_time_sec"] += 1.5
        agt["time_remaining_sec"] = agt["max_time_sec"]
        
        audit_logs.append({
            "event_id": f"evt_{len(audit_logs)+1}",
            "action": "AUTONOMOUS_SKILL_EVOLUTION",
            "agent": agt["name"],
            "new_level": agt["skill_level"],
            "new_response_time_ms": agt["response_time_ms"]
        })

# LOOP AUTÔNOMO: EVOLUÇÃO AUTÔNOMA DE SKILLS + BARRA DE VIDA/TIMEOUT + ATUALIZAÇÃO KANBAN
async def autonomous_orchestration_game_loop():
    po_turn_duration = 60      
    heroes_turn_duration = 120 
    
    while True:
        # =========================================================================
        # FASE 1: TURNO DO PO VILÃO (1 MINUTO - PRIORIDADE NO GEMMA 4)
        # =========================================================================
        game_state["current_turn"] = "PO_BURST_PHASE"
        game_state["boss_cards_created_in_burst"] = 0
        
        for agt in pixel_agents.values():
            agt["can_use_gemma"] = False
            agt["action"] = "🔒 PO com Prioridade no Gemma 4 (Aguardando...)"

        for sec in range(po_turn_duration, 0, -1):
            if game_state["victory"]: break
            game_state["turn_timer_sec"] = sec
            
            # Atualiza o decaimento do tempo de resposta (VIDA/TIMEOUT) dos heróis a cada segundo
            for agt_key, agt in pixel_agents.items():
                decay = (agt["response_time_ms"] / 400.0) * 0.6
                agt["time_remaining_sec"] = max(0.0, round(agt["time_remaining_sec"] - decay, 1))
                
                # Se o tempo zera, ocorre o Timeout, mas a Skill Auto-Heal recupera!
                if agt["time_remaining_sec"] <= 0:
                    agt["time_remaining_sec"] = round(agt["max_time_sec"] * 0.5, 1)
                    audit_logs.append({
                        "event_id": f"evt_{len(audit_logs)+1}",
                        "action": "TIMEOUT_AUTO_HEAL",
                        "agent": agt["name"],
                        "note": "Skill autônoma evitou o Timeout!"
                    })

            # PO cria os 5 cards no 'A FAZER'
            if game_state["boss_cards_created_in_burst"] < 5 and sec % 10 == 0:
                po_topics = [
                    ("Refatorar UI Frontend Nível Pixel Perfect 16-Bit", "O PO Vilão analisou a interface atual e exige alinhamento perfeito de bordas, palette HSL e suporte responsive sem flickering."),
                    ("Otimização de Performance Backend Async & Caching", "Cobrança do PO: Reduzir a latência do EventBus para <5ms e adicionar suporte a cache Redis com TTL dinâmico."),
                    ("Auditoria Anti-Alucinação e Cobertura de Testes Mutation", "Exigência do PO: Adicionar testes de mutação com cobertura 100% comprovada via evidência SHA-256 no log imutável."),
                    ("CONTRATAÇÃO: Onboarding de Desenvolvedor Frontend Senior", "Demanda de RH do PO: Recrutar colaborador especialista em React e Pixel Art Canvas."),
                    ("Sanitização Estrita contra Vulnerabilidades XSS & SQL", "O PO encontrou potenciais falhas de segurança nos endpoints REST.")
                ]
                topic_title, topic_desc = po_topics[game_state["boss_cards_created_in_burst"] % len(po_topics)]
                
                gemma_ideas = gemma.generate_ideas(topic_title)
                idea_detail = gemma_ideas[0]["summary"] if gemma_ideas else topic_desc

                jira_res = jira.create_detailed_epic_or_task("KAN", topic_title, idea_detail, "ÉPICO PO GEMMA4")
                new_key = jira_res.get("key", f"KAN-{random.randint(9700, 9999)}")
                
                new_card = {
                    "id": new_key,
                    "title": f"[PO-GEMMA4] {topic_title}",
                    "description": idea_detail,
                    "status": "A FAZER",
                    "rejections": 0,
                    "comments": [{"author": "PO EVIL BOSS", "text": f"Criado com Gemma 4 no 'A FAZER': {topic_title}."}]
                }
                game_state["kanban"]["to_do"].append(new_card)
                game_state["boss_cards_created_in_burst"] += 1
                game_state["boss_phase"] = f"🔥 PO RAJADA GEMMA 4 ({game_state['boss_cards_created_in_burst']}/5): CRIOU CARD REAL {new_key} NO JIRA!"

            await asyncio.sleep(1.0)

        # =========================================================================
        # FASE 2: TURNO DOS HERÓIS (2 MINUTOS - CLAUDE-CODE OLLAMA & AGY CLI & EVOLUÇÃO AUTÔNOMA)
        # =========================================================================
        game_state["current_turn"] = "HEROES_REST_PHASE"
        game_state["boss_phase"] = "😴 PO DESCANSA! HERÓIS OPERANDO CLAUDE-CODE OLLAMA E EVOLUINDO SKILLS!"

        for agt in pixel_agents.values():
            agt["can_use_gemma"] = True
            agt["action"] = f"⚡ Evoluindo Skill (Nível {agt['skill_level']} - {agt['response_time_ms']}ms)"

        for sec in range(heroes_turn_duration, 0, -1):
            if game_state["victory"]: break
            game_state["turn_timer_sec"] = sec

            # Decaimento do tempo de vida / timeout
            for agt in pixel_agents.values():
                decay = (agt["response_time_ms"] / 400.0) * 0.5
                agt["time_remaining_sec"] = max(0.0, round(agt["time_remaining_sec"] - decay, 1))
                if agt["time_remaining_sec"] <= 0:
                    agt["time_remaining_sec"] = round(agt["max_time_sec"] * 0.5, 1)

            # PASSO A: Mover do 'A Fazer' para 'Em Validação'
            if game_state["kanban"]["to_do"] and not game_state["kanban"]["in_progress"]:
                card = game_state["kanban"]["to_do"].pop(0)
                card["status"] = "EM PROGRESSO"
                game_state["kanban"]["in_progress"].append(card)
                game_state["current_working_card"] = card

                # Heróis usam Claude-Code Ollama & AGY e evoluem a skill autonomamente!
                active_agent_key = random.choice(["felipe", "sofia", "lucas", "beatriz"])
                check_autonomous_skill_evolution(active_agent_key)
                active_agt = pixel_agents[active_agent_key]

                solutions = gemma.generate_ideas(card["title"])
                sol_text = solutions[0]["summary"] if solutions else "Análise de alta velocidade via Ollama."

                card["comments"].append({"author": f"{active_agt['name']} (Lv.{active_agt['skill_level']})", "text": f"🛠️ Executou patch via Claude-Code Ollama & AGY em {active_agt['response_time_ms']}ms. Movendo para 'EM VALIDAÇÃO'!"})
                jira.add_comment(card["id"], active_agt['name'], f"Patch de velocidade {active_agt['response_time_ms']}ms aplicado. Movendo para Em Validação.")

                game_state["kanban"]["in_progress"].remove(card)
                card["status"] = "EM VALIDAÇÃO"
                game_state["kanban"]["in_validation"].append(card)

            # PASSO B: Validação do PO
            if game_state["kanban"]["in_validation"]:
                card_val = game_state["kanban"]["in_validation"].pop(0)
                
                if random.random() < 0.20 and card_val["rejections"] == 0:
                    card_val["rejections"] += 1
                    card_val["status"] = "A FAZER"
                    card_val["comments"].append({"author": "PO EVIL BOSS", "text": "❌ BARRADO! Volte para o 'A FAZER'!"})
                    jira.add_comment(card_val["id"], "PO EVIL BOSS", "Barrado na Validação.")
                    game_state["kanban"]["to_do"].append(card_val)
                else:
                    card_val["status"] = "CONCLUÍDO"
                    card_val["comments"].append({"author": "PO EVIL BOSS", "text": "✅ Aprovado na Validação Rígida!"})
                    jira.add_comment(card_val["id"], "PO EVIL BOSS", "Card Aprovado.")

                    damage = 250
                    game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                    game_state["kanban"]["done"].append(card_val)
                    game_state["cards_coded_count"] += 1

                    # Restaura o tempo de vida/timeout dos heróis ao resolver o card!
                    for agt in pixel_agents.values():
                        agt["time_remaining_sec"] = agt["max_time_sec"]

                    h = governance.generate_audit_hash("agt_lucas", "AUTONOMOUS_EVOLVED_CARD_APPROVED", card_val['title'])
                    audit_logs.append({
                        "event_id": f"evt_{len(audit_logs)+1}",
                        "action": "AUTONOMOUS_CARD_CLOSED",
                        "card_id": card_val["id"],
                        "damage": damage,
                        "boss_hp": game_state["boss_hp"],
                        "hash": h,
                    })

                    if game_state["boss_hp"] <= 0:
                        game_state["victory"] = True
                        game_state["boss_phase"] = "🏆 VITÓRIA! OS HERÓIS EVOLUÍRAM SUAS SKILLS E DERROTARAM O PO VILÃO!"

            await asyncio.sleep(1.0)

@app.on_event("startup")
async def start_autonomous_loop():
    await bus.start()
    asyncio.create_task(autonomous_orchestration_game_loop())

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
        "kanban": game_state["kanban"],
        "current_card": game_state["current_working_card"],
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
        <title>FLOSE AEOS - Real-Time Kanban & Autonomous Skill Evolution</title>
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
                width: 550px;
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
                min-height: 120px;
            }

            .kanban-col-title {
                font-size: 0.42rem;
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
                font-size: 0.4rem;
                line-height: 1.3;
            }

            .time-bar-bg {
                width: 100%;
                height: 8px;
                background: #440000;
                border: 1px solid #ff5555;
                border-radius: 3px;
                margin-top: 0.2rem;
                overflow: hidden;
            }

            .time-bar-fill {
                height: 100%;
                background: #00ff00;
                transition: width 0.3s linear;
            }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>

            <div class="side-panel">
                <div>
                    <div class="hud-title">⚡ REAL-TIME KANBAN & EVOLUÇÃO AUTÔNOMA</div>
                    
                    <div id="turn-banner" class="turn-banner">
                        TURNO ATUAL: CARREGANDO...
                    </div>

                    <!-- QUADRO KANBAN ATUALIZANDO EM TEMPO REAL -->
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

                    <div style="font-size:0.48rem; color:#a855f7; margin-bottom:0.4rem;">🛡️ EVOLUÇÃO AUTÔNOMA DE SKILL & VIDA (TIMEOUT):</div>
                    <div id="skills-list">Carregando heróis...</div>
                </div>

                <div>
                    <div style="font-size: 0.45rem; color: #55ff55; margin-bottom: 0.3rem;">📜 AUDIT LOG JIRA REAL</div>
                    <div id="audit-log" style="font-size: 0.4rem; color: #9ca3af; max-height: 80px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('pixel-canvas');
            const ctx = canvas.getContext('2d');

            function resizeCanvas() {
                canvas.width = window.innerWidth - 550;
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];

            function drawPixelSprite(x, y, color, name, respMs, timeLeft, maxTime, lvl) {
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

                // Barra de Vida = Tempo Restante antes do Timeout!
                const pct = Math.max(0, (timeLeft / maxTime) * 100);
                ctx.fillStyle = "#440000";
                ctx.fillRect(x - 6, y - 6, 36, 4);
                ctx.fillStyle = pct > 40 ? "#00ff00" : "#ff5555";
                ctx.fillRect(x - 6, y - 6, (36 * pct) / 100, 4);

                ctx.font = '5px "Press Start 2P"';
                ctx.fillStyle = "#55ffff";
                ctx.fillText(`${respMs.toFixed(0)}ms | ${timeLeft.toFixed(1)}s`, x - 15, y + 38);
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
                    drawPOBoss(hpPct, gameState.boss_phase || "Atualizando Quadro...");

                    agentsList.forEach(a => {
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, a.response_time_ms, a.time_remaining_sec, a.max_time_sec, a.skill_level);
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
                const kanban = data.kanban;

                const isPoTurn = gameState.current_turn === "PO_BURST_PHASE";
                document.getElementById('turn-banner').style.borderColor = isPoTurn ? "#ff5555" : "#55ff55";
                document.getElementById('turn-banner').style.color = isPoTurn ? "#ff5555" : "#55ff55";
                document.getElementById('turn-banner').innerHTML = isPoTurn ?
                    `👹 TURNO PO: GEMMA 4 (5 CARDS JIRA) | ⏱️ ${gameState.turn_timer_sec}s` :
                    `⚡ TURNO HERÓIS: CLAUDE-CODE & EVOLUÇÃO SKILL | ⏱️ ${gameState.turn_timer_sec}s`;

                // Render Quadro Kanban em Tempo Real
                document.getElementById('col-todo').innerHTML = kanban.to_do.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#ff5555; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 16)}...</div>
                    </div>
                `).join('');

                document.getElementById('col-validation').innerHTML = kanban.in_validation.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#ffaa00; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 16)}...</div>
                    </div>
                `).join('');

                document.getElementById('col-done').innerHTML = kanban.done.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#55ff55; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 16)}...</div>
                    </div>
                `).join('');

                // Render Evolução Autônoma das Skills e Vida/Timeout dos Agentes
                document.getElementById('skills-list').innerHTML = agentsList.map(a => {
                    const pct = Math.max(0, (a.time_remaining_sec / a.max_time_sec) * 100);
                    return `
                        <div style="background:rgba(0,0,0,0.5); border:1px solid #30363d; padding:0.4rem; border-radius:4px; margin-bottom:0.3rem; font-size:0.42rem;">
                            <div style="color:${a.sprite_color}; font-weight:bold;">${a.name} (Lv.${a.skill_level}) <span style="float:right; color:#a855f7;">XP: ${a.xp}%</span></div>
                            <div style="color:#9ca3af; margin-top:0.2rem;">Latência: <span style="color:#55ffff;">${a.response_time_ms.toFixed(0)}ms</span> | Timeout: ${a.time_remaining_sec.toFixed(1)}s</div>
                            <div class="time-bar-bg">
                                <div class="time-bar-fill" style="width:${pct}%; background:${pct < 40 ? '#ff5555' : '#00ff00'};"></div>
                            </div>
                        </div>
                    `;
                }).join('');

                document.getElementById('audit-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.2rem;">> ${l.action}: ${l.agent || l.card_id || ''}</div>
                `).join('');
            }

            updateState();
            setInterval(updateState, 500); // Polling ultra-rápido de 500ms para tempo real perfeito!
        </script>
    </body>
    </html>
    """
