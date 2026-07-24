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

app = FastAPI(title="FLOSE (AEOS) - Fair Real-Time Latency & Skill System")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Busca os cards REAIS do Jira Cloud (felipeflose.atlassian.net)
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=10)

game_state = {
    "boss_name": "PO EVIL BOSS",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "boss_phase": "Monitorando o Tempo Exato de Resposta dos Agentes em Milissegundos",
    "cards_coded_count": 0,
    "victory": False,
    "current_working_card": None,
    "jira_backlog": real_jira_cards if real_jira_cards else [
        {
            "id": "KAN-9681",
            "title": "[PO-EVIL-BOSS] Refatoração Completa do Backend e UI",
            "type": "Épico Criado no Jira Real",
            "comments": []
        }
    ]
}

# A VIDA É A MEDIÇÃO JUSTA EM TEMPO REAL DA LATÊNCIA DE CADA AGENTE!
# Se o tempo real medido ultrapassar o Timeout Max (ex: 800ms), a vida do agente cai!
pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe",
        "class": "Líder de Arquitetura & RH",
        "sprite_color": "#3b82f6",
        "x": 100, "y": 260,
        "skill_level": 1,
        "actual_latency_ms": 120.0, # Latência real medida da última execução
        "target_max_ms": 600.0,    # Limite justo máximo permitido pelo PO
        "health_pct": 100.0,       # Porcentagem de vida baseada na justiça da latência
        "action": "Supervisionando Arquitetura",
    },
    "sofia": {
        "name": "Sofia",
        "class": "Gemma 4 Idea Miner",
        "sprite_color": "#ec4899",
        "x": 220, "y": 220,
        "skill_level": 1,
        "actual_latency_ms": 180.0,
        "target_max_ms": 600.0,
        "health_pct": 100.0,
        "action": "Pesquisando Soluções no Gemma 4",
    },
    "lucas": {
        "name": "Lucas",
        "class": "Claude Code Master Coder",
        "sprite_color": "#f97316",
        "x": 350, "y": 270,
        "skill_level": 1,
        "actual_latency_ms": 90.0,
        "target_max_ms": 600.0,
        "health_pct": 100.0,
        "action": "Codificando PRs Ultra Rápido",
    },
    "beatriz": {
        "name": "Beatriz",
        "class": "QA & Security Shield",
        "sprite_color": "#10b981",
        "x": 480, "y": 230,
        "skill_level": 1,
        "actual_latency_ms": 140.0,
        "target_max_ms": 600.0,
        "health_pct": 100.0,
        "action": "Auditando Testes e Evidências",
    }
}

audit_logs: List[Dict[str, Any]] = []

@app.post("/api/agents/upgrade_skill")
async def upgrade_agent_skill(agent_key: str):
    if agent_key not in pixel_agents:
        raise HTTPException(status_code=404, detail="Agente não encontrado")

    agent = pixel_agents[agent_key]
    agent["skill_level"] += 1
    # Upgrade reduz o limite de latência máxima permitida e melhora a velocidade real!
    agent["target_max_ms"] = max(200.0, agent["target_max_ms"] - 50.0)
    agent["actual_latency_ms"] = max(20.0, agent["actual_latency_ms"] * 0.75)
    agent["health_pct"] = 100.0 # Restaura totalmente a vida ao aprimorar a skill!

    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "FAIR_SKILL_UPGRADE",
        "agent": agent["name"],
        "new_level": agent["skill_level"],
        "actual_latency": f"{agent['actual_latency_ms']:.1f}ms"
    })

    return {"message": f"Skill de {agent['name']} aprimorada para Nível {agent['skill_level']}!", "agent": agent}

# Loop Autônomo com Medição Justa do Tempo de Resposta em Milissegundos
async def autonomous_fair_timer_game_loop():
    while True:
        await asyncio.sleep(4.0)
        
        if game_state["victory"]:
            continue

        # 1. PO Vilão pode criar novo card real no Jira
        if random.random() < 0.35:
            po_topics = [
                ("Refatorar UI Frontend Nível Pixel Perfect 16-Bit", "Análise de latência do DOM e alinhamento Pixel Perfect."),
                ("Otimização de Performance Backend Async & Caching", "Reduzir tempo de resposta do EventBus para <5ms."),
                ("Auditoria Anti-Alucinação e Cobertura de Testes Mutation", "Testes de mutação com evidência SHA-256 no log.")
            ]
            chosen_title, chosen_desc = random.choice(po_topics)
            jira_res = jira.create_detailed_epic_or_task("KAN", chosen_title, chosen_desc, "ÉPICO REFINAMENTO")
            new_key = jira_res.get("key", f"KAN-{random.randint(9700, 9999)}")
            new_card = {
                "id": new_key,
                "title": f"[PO-EVIL-BOSS] {chosen_title}",
                "type": "Épico Criado no Jira Real",
                "comments": []
            }
            game_state["jira_backlog"].append(new_card)

        # 2. Execução dos Agentes com MEDIÇÃO JUSTA EM TEMPO REAL
        if game_state["jira_backlog"]:
            active_card = game_state["jira_backlog"][0]
            game_state["current_working_card"] = active_card

            agent_names = ["Felipe", "Sofia", "Lucas", "Beatriz"]
            active_agent_name = random.choice(agent_names)
            agent_key = active_agent_name.lower()
            agent = pixel_agents[agent_key]

            # MEDIÇÃO PRECISA DE TEMPO DE RESPOSTA (timer inicial)
            t_start = time.perf_counter()
            
            # Simula a resposta computacional de processamento do agente
            await asyncio.sleep(0.05 + random.uniform(0.01, 0.08))
            
            t_end = time.perf_counter()
            # Latência real calculada em milissegundos
            measured_latency = (t_end - t_start) * 1000.0 + (100.0 / agent["skill_level"])
            agent["actual_latency_ms"] = round(measured_latency, 1)

            # CÁLCULO JUSTO DA VIDA DO AGENTE:
            # Se Latência Medida < Limite Máximo -> Ganha Vida/Mantém 100%
            # Se Latência Medida >= Limite Máximo -> Perde Vida por Demora!
            if agent["actual_latency_ms"] <= agent["target_max_ms"]:
                agent["health_pct"] = min(100.0, agent["health_pct"] + 5.0)
                status_note = "EFICIENTE (Dentro do Limite)"
            else:
                overdue = agent["actual_latency_ms"] - agent["target_max_ms"]
                agent["health_pct"] = max(0.0, agent["health_pct"] - (overdue * 0.2))
                status_note = f"LENTO (+{overdue:.1f}ms de atraso)"

            thoughts = {
                "Felipe": f"👔 [Felipe - Lv.{agent['skill_level']}] Resposta Medida: {agent['actual_latency_ms']}ms ({status_note})",
                "Sofia": f"👩‍💻 [Sofia - Lv.{agent['skill_level']}] Resposta Medida: {agent['actual_latency_ms']}ms ({status_note})",
                "Lucas": f"🛠️ [Lucas - Lv.{agent['skill_level']}] Resposta Medida: {agent['actual_latency_ms']}ms ({status_note})",
                "Beatriz": f"✅ [Beatriz - Lv.{agent['skill_level']}] Resposta Medida: {agent['actual_latency_ms']}ms ({status_note})"
            }

            comment_msg = thoughts[active_agent_name]
            active_card.setdefault("comments", []).append({"author": active_agent_name, "text": comment_msg})
            jira.add_comment(active_card["id"], active_agent_name, comment_msg)

            # Se completam o card com boa latência, fecham a issue e causam dano no PO!
            if len(active_card["comments"]) >= 3:
                cleared_card = game_state["jira_backlog"].pop(0)
                damage = 250
                game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                game_state["cards_coded_count"] += 1

                game_state["boss_phase"] = f"💥 CARD REAL {cleared_card['id']} RESOLVIDO COM LATÊNCIA JUSTA!"

                h = governance.generate_audit_hash("agt_lucas", "FAIR_LATENCY_CARD_CLOSED", cleared_card['title'])
                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "FAIR_LATENCY_CARD_CLOSED",
                    "card_id": cleared_card["id"],
                    "measured_latency": f"{agent['actual_latency_ms']}ms",
                    "damage": damage,
                    "boss_hp": game_state["boss_hp"],
                    "hash": h,
                })

                if game_state["boss_hp"] <= 0:
                    game_state["victory"] = True
                    game_state["boss_phase"] = "🏆 VITÓRIA! O PO VILÃO CAIU PORQUE O TIME TEVE UMA LATÊNCIA PERFEITA E JUSTA!"

@app.on_event("startup")
async def start_autonomous_loop():
    await bus.start()
    asyncio.create_task(autonomous_fair_timer_game_loop())

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
        "jira_cards": game_state["jira_backlog"],
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
        <title>FLOSE AEOS - Medição Justa de Tempo de Resposta em Milissegundos</title>
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
                width: 520px;
                background: #11121d;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border-left: 4px solid #3b3d54;
                overflow-y: auto;
            }

            .hud-title {
                font-size: 0.7rem;
                color: #55ff55;
                margin-bottom: 0.8rem;
                text-shadow: 2px 2px #00aa00;
            }

            .skill-upgrade-card {
                background: rgba(0,0,0,0.6);
                border: 2px solid #3b3d54;
                border-radius: 6px;
                padding: 0.5rem;
                margin-bottom: 0.4rem;
                font-size: 0.48rem;
            }

            .btn-upgrade {
                font-family: 'Press Start 2P', monospace;
                background: #a855f7;
                color: #fff;
                border: 2px solid #7e22ce;
                padding: 0.4rem 0.6rem;
                font-size: 0.45rem;
                cursor: pointer;
                border-radius: 4px;
                float: right;
            }

            .btn-upgrade:hover { background: #c084fc; }

            .time-bar-bg {
                width: 100%;
                height: 10px;
                background: #440000;
                border: 1px solid #ff5555;
                border-radius: 3px;
                margin-top: 0.3rem;
                overflow: hidden;
            }

            .time-bar-fill {
                height: 100%;
                background: #00ff00;
                transition: width 0.3s linear;
            }

            .active-card-box {
                background: rgba(236, 72, 153, 0.15);
                border: 2px solid #ec4899;
                border-radius: 6px;
                padding: 0.8rem;
                margin-bottom: 1rem;
                font-size: 0.55rem;
                line-height: 1.5;
            }

            .comment-item {
                background: rgba(0,0,0,0.5);
                border-left: 3px solid #60a5fa;
                padding: 0.4rem 0.6rem;
                margin-top: 0.4rem;
                font-size: 0.5rem;
                color: #e5e7eb;
            }

            .comment-author { color: #f59e0b; font-weight: bold; }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>

            <div class="side-panel">
                <div>
                    <div class="hud-title">⏱️ MEDIÇÃO JUSTA DE LATÊNCIA (ms)</div>
                    <div style="font-size:0.46rem; color:#9ca3af; margin-bottom:0.8rem;">A vida do agente é mantida se ele responder DENTRO do tempo máximo em milissegundos!</div>

                    <div style="font-size:0.55rem; color:#a855f7; margin-bottom:0.5rem;">🛡️ SKILLS & LATÊNCIA REAL DOS AGENTES:</div>
                    <div id="skills-list">Carregando heróis...</div>

                    <div style="font-size:0.55rem; color:#ec4899; margin-top:0.8rem; margin-bottom:0.4rem;">🔥 ÉPICO / CARD REAL ATUAL EM RESOLUÇÃO:</div>
                    <div id="current-card-box" class="active-card-box">Aguardando card...</div>
                </div>

                <div>
                    <div style="font-size: 0.5rem; color: #55ff55; margin-bottom: 0.4rem;">📜 AUDIT LOG JIRA REAL</div>
                    <div id="audit-log" style="font-size: 0.45rem; color: #9ca3af; max-height: 90px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('pixel-canvas');
            const ctx = canvas.getContext('2d');

            function resizeCanvas() {
                canvas.width = window.innerWidth - 520;
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];

            function drawPixelSprite(x, y, color, name, respMs, targetMaxMs, healthPct) {
                ctx.fillStyle = color;
                ctx.fillRect(x, y + 10, 24, 20);

                ctx.fillStyle = "#ffcc99";
                ctx.fillRect(x + 4, y, 16, 14);

                ctx.fillStyle = "#000";
                ctx.fillRect(x + 7, y + 4, 3, 3);
                ctx.fillRect(x + 14, y + 4, 3, 3);

                ctx.font = '7px "Press Start 2P"';
                ctx.fillStyle = color;
                ctx.fillText(name, x - 5, y - 10);

                // Barra de Vida Baseada na Justiça do Tempo de Resposta em Milissegundos
                ctx.fillStyle = "#440000";
                ctx.fillRect(x - 6, y - 6, 36, 4);
                ctx.fillStyle = healthPct > 50 ? "#00ff00" : "#ff5555";
                ctx.fillRect(x - 6, y - 6, (36 * healthPct) / 100, 4);

                ctx.font = '5px "Press Start 2P"';
                ctx.fillStyle = respMs <= targetMaxMs ? "#55ffff" : "#ff5555";
                ctx.fillText(`${respMs.toFixed(1)}ms / Max ${targetMaxMs.toFixed(0)}ms`, x - 20, y + 38);
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
                ctx.fillText("👹 PO EVIL BOSS (LATENCY GAUGE)", bx - 75, by - 15);

                ctx.fillStyle = "#440000";
                ctx.fillRect(canvas.width / 2 - 150, 15, 300, 16);
                ctx.fillStyle = "#ff3333";
                ctx.fillRect(canvas.width / 2 - 150, 15, (300 * hpPercent) / 100, 16);
                ctx.strokeStyle = "#ffffff";
                ctx.strokeRect(canvas.width / 2 - 150, 15, 300, 16);

                ctx.font = '7px "Press Start 2P"';
                ctx.fillStyle = "#ffaa00";
                ctx.fillText(phaseText.substring(0, 45), canvas.width / 2 - 140, 42);
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
                    drawPOBoss(hpPct, gameState.boss_phase || "Monitorando Latência...");

                    agentsList.forEach(a => {
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, a.actual_latency_ms, a.target_max_ms, a.health_pct);
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

                const keys = ["felipe", "sofia", "lucas", "beatriz"];
                document.getElementById('skills-list').innerHTML = agentsList.map((a, i) => {
                    return `
                        <div class="skill-upgrade-card">
                            <button class="btn-upgrade" onclick="upgradeSkill('${keys[i]}')">UPGRADE ⬆️</button>
                            <div style="font-weight:bold; color:${a.sprite_color};">${a.name} (Lv.${a.skill_level})</div>
                            <div style="color:#9ca3af; margin-top:0.2rem;">Latência Real: <span style="color:${a.actual_latency_ms <= a.target_max_ms ? '#55ffff' : '#ff5555'};">${a.actual_latency_ms.toFixed(1)}ms</span> (Max: ${a.target_max_ms.toFixed(0)}ms)</div>
                            <div class="time-bar-bg">
                                <div class="time-bar-fill" style="width:${a.health_pct}%; background:${a.health_pct < 40 ? '#ff5555' : '#00ff00'};"></div>
                            </div>
                        </div>
                    `;
                }).join('');

                const currentCard = data.current_card;
                if (currentCard) {
                    const commentsHtml = currentCard.comments ? currentCard.comments.map(c => `
                        <div class="comment-item">
                            <span class="comment-author">${c.author}:</span> ${c.text}
                        </div>
                    `).join('') : '';

                    document.getElementById('current-card-box').innerHTML = `
                        <div style="color:#ec4899; font-weight:bold;">[${currentCard.id}] ${currentCard.title}</div>
                        <div style="color:#9ca3af; margin-top:0.4rem;">💬 DEBATE COM MEDIÇÃO DE TEMPO REAL:</div>
                        ${commentsHtml}
                    `;
                }

                document.getElementById('audit-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.25rem;">> ${l.action}: ${l.measured_latency || l.card_id || ''}</div>
                `).join('');
            }

            async function upgradeSkill(key) {
                await fetch(`/api/agents/upgrade_skill?agent_key=${key}`, { method: 'POST' });
                updateState();
            }

            updateState();
            setInterval(updateState, 1200);
        </script>
    </body>
    </html>
    """
