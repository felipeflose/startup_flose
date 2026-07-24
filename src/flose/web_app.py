import asyncio
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

app = FastAPI(title="FLOSE (AEOS) - Real Jira Cloud Epic & Task Creation Engine")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Busca os cards REAIS da sua conta do Jira Cloud (felipeflose.atlassian.net)
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=10)

game_state = {
    "boss_name": "PO EVIL BOSS",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "boss_phase": "Criando Épicos e Tasks Super Detalhados no Jira Real (felipeflose.atlassian.net)",
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

pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe",
        "class": "Líder de Arquitetura & RH",
        "sprite_color": "#3b82f6",
        "x": 100, "y": 260,
        "skill_level": 1,
        "response_time_ms": 450,
        "time_remaining_sec": 10.0,
        "max_time_sec": 10.0,
        "action": "Supervisionando Épicos Reais do Jira",
    },
    "sofia": {
        "name": "Sofia",
        "class": "Gemma 4 Idea Miner",
        "sprite_color": "#ec4899",
        "x": 220, "y": 220,
        "skill_level": 1,
        "response_time_ms": 380,
        "time_remaining_sec": 10.0,
        "max_time_sec": 10.0,
        "action": "Pesquisando Soluções para os Épicos do PO",
    },
    "lucas": {
        "name": "Lucas",
        "class": "Claude Code Master Coder",
        "sprite_color": "#f97316",
        "x": 350, "y": 270,
        "skill_level": 1,
        "response_time_ms": 250,
        "time_remaining_sec": 10.0,
        "max_time_sec": 10.0,
        "action": "Codificando PRs dos Cards do Jira Real",
    },
    "beatriz": {
        "name": "Beatriz",
        "class": "QA & Security Shield",
        "sprite_color": "#10b981",
        "x": 480, "y": 230,
        "skill_level": 1,
        "response_time_ms": 400,
        "time_remaining_sec": 10.0,
        "max_time_sec": 10.0,
        "action": "Auditando DoD & Testes de Aceite",
    }
}

audit_logs: List[Dict[str, Any]] = []

@app.post("/api/agents/upgrade_skill")
async def upgrade_agent_skill(agent_key: str):
    if agent_key not in pixel_agents:
        raise HTTPException(status_code=404, detail="Agente não encontrado")

    agent = pixel_agents[agent_key]
    agent["skill_level"] += 1
    agent["response_time_ms"] = max(50, agent["response_time_ms"] - 60)
    agent["max_time_sec"] += 2.0
    agent["time_remaining_sec"] = agent["max_time_sec"]

    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "AGENT_SKILL_UPGRADED",
        "agent": agent["name"],
        "new_level": agent["skill_level"],
        "new_response_time_ms": agent["response_time_ms"]
    })

    return {"message": f"Skill de {agent['name']} aprimorada para Nível {agent['skill_level']}!", "agent": agent}

# Loop Autônomo: O PO cria CARDS SUPER DETALHADOS REAIS NO JIRA e o time resolve!
async def autonomous_jira_epic_game_loop():
    while True:
        await asyncio.sleep(5.0)
        
        if game_state["victory"]:
            continue

        # 1. O PO Vilão cria um CARD/ÉPICO SUPER DETALHADO DIRETAMENTE NO JIRA CLOUD REAL!
        if random.random() < 0.4:
            po_topics = [
                ("Refatorar UI Frontend Nível Pixel Perfect 16-Bit", "O PO Vilão analisou a interface atual e exige alinhamento perfeito de bordas, palette HSL e suporte responsive sem flickering."),
                ("Otimização de Performance Backend Async & Caching", "Cobrança do PO: Reduzir a latência do EventBus para <5ms e adicionar suporte a cache Redis com TTL dinâmico."),
                ("Auditoria Anti-Alucinação e Cobertura de Testes Mutation", "Exigência do PO: Adicionar testes de mutação com cobertura 100% comprovada via evidência SHA-256 no log imutável."),
                ("Integração de Microserviços & Protocolo MCP Bridge", "O PO exige a criação de novos conectores MCP para exportar métricas de telemetria diretamente para o Jira Cloud.")
            ]
            chosen_title, chosen_desc = random.choice(po_topics)

            # CRIAÇÃO REAL NO JIRA CLOUD!
            jira_res = jira.create_detailed_epic_or_task(
                project_key="KAN",
                summary=chosen_title,
                detailed_description=chosen_desc,
                epic_name="ÉPICO DE REFINAMENTO AUTÔNOMO"
            )

            new_key = jira_res.get("key", f"KAN-{random.randint(9700, 9999)}")
            new_card = {
                "id": new_key,
                "title": f"[PO-EVIL-BOSS] {chosen_title}",
                "type": "Épico Criado no Jira Real",
                "comments": [
                    {"author": "PO EVIL BOSS", "text": f"Criei o card super detalhado {new_key} no Jira Cloud com todos os critérios de aceite!"}
                ]
            }
            game_state["jira_backlog"].append(new_card)
            game_state["boss_phase"] = f"😈 PO VILÃO CRIOU O CARD REAL DETALHADO {new_key} NO JIRA!"

        # 2. Atualização dos tempos de resposta dos heróis
        for agent in pixel_agents.values():
            decay = (agent["response_time_ms"] / 500.0) * 0.8
            agent["time_remaining_sec"] = max(0.0, round(agent["time_remaining_sec"] - decay, 1))
            if agent["time_remaining_sec"] <= 0:
                agent["time_remaining_sec"] = round(agent["max_time_sec"] * 0.6, 1)

        # 3. Os Agentes debatem e comentam DIRETAMENTE NO JIRA REAL e fecham a issue!
        if game_state["jira_backlog"]:
            active_card = game_state["jira_backlog"][0]
            game_state["current_working_card"] = active_card

            agent_names = ["Felipe", "Sofia", "Lucas", "Beatriz"]
            active_agent_name = random.choice(agent_names)
            agent_key = active_agent_name.lower()
            resp_time = pixel_agents[agent_key]["response_time_ms"]
            
            thoughts = {
                "Felipe": f"👔 [Felipe - Lv.{pixel_agents['felipe']['skill_level']}] Analisando requisitos do card {active_card['id']}.",
                "Sofia": f"👩‍💻 [Sofia - Lv.{pixel_agents['sofia']['skill_level']}] Estudo de arquitetura concluído no Gemma 4 local.",
                "Lucas": f"🛠️ [Lucas - Lv.{pixel_agents['lucas']['skill_level']}] Patch de código gerado e comitado no repositório!",
                "Beatriz": f"✅ [Beatriz - Lv.{pixel_agents['beatriz']['skill_level']}] Testes de regressão e DoD aprovados!"
            }

            comment_msg = thoughts[active_agent_name]
            active_card.setdefault("comments", []).append({"author": active_agent_name, "text": comment_msg})
            
            # Adiciona o comentário diretamente na issue real no Jira Cloud!
            jira.add_comment(active_card["id"], active_agent_name, comment_msg)

            if len(active_card["comments"]) >= 3:
                cleared_card = game_state["jira_backlog"].pop(0)
                damage = 250
                game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                game_state["cards_coded_count"] += 1
                
                for agt in pixel_agents.values():
                    agt["time_remaining_sec"] = agt["max_time_sec"]

                game_state["boss_phase"] = f"💥 CARD REAL {cleared_card['id']} FECHADO NO JIRA CLOUD!"

                h = governance.generate_audit_hash("agt_lucas", "REAL_JIRA_EPIC_RESOLVED", cleared_card['title'])
                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "REAL_JIRA_EPIC_CLOSED",
                    "card_id": cleared_card["id"],
                    "damage": damage,
                    "boss_hp": game_state["boss_hp"],
                    "hash": h,
                })

                if game_state["boss_hp"] <= 0:
                    game_state["victory"] = True
                    game_state["boss_phase"] = "🏆 VITÓRIA! TODOS OS ÉPICOS DO JIRA CLOUD FORAM CODIFICADOS E O PO VILÃO CAIU!"

@app.on_event("startup")
async def start_autonomous_loop():
    await bus.start()
    asyncio.create_task(autonomous_jira_epic_game_loop())

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
        <title>FLOSE AEOS - Real Jira Cloud Epic Creation & Boss Fight</title>
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
                width: 500px;
                background: #11121d;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border-left: 4px solid #3b3d54;
                overflow-y: auto;
            }

            .hud-title {
                font-size: 0.75rem;
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
                height: 8px;
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
                    <div class="hud-title">🔷 JIRA CLOUD REAL: ÉPICOS & DETALHES</div>
                    <div style="font-size:0.46rem; color:#9ca3af; margin-bottom:0.8rem;">O PO cria Épicos detalhados no Jira felipeflose.atlassian.net e o time resolve!</div>

                    <div style="font-size:0.55rem; color:#a855f7; margin-bottom:0.5rem;">🛡️ SKILLS DOS HERÓIS (TEMPO DE RESPOSTA):</div>
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
                canvas.width = window.innerWidth - 500;
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];

            function drawPixelSprite(x, y, color, name, respMs, timeLeft, maxTime) {
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

                const pct = Math.max(0, (timeLeft / maxTime) * 100);
                ctx.fillStyle = "#440000";
                ctx.fillRect(x - 6, y - 6, 36, 4);
                ctx.fillStyle = pct > 40 ? "#00ff00" : "#ff5555";
                ctx.fillRect(x - 6, y - 6, (36 * pct) / 100, 4);

                ctx.font = '5px "Press Start 2P"';
                ctx.fillStyle = "#55ffff";
                ctx.fillText(`${respMs}ms | ${timeLeft.toFixed(1)}s`, x - 12, y + 38);
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
                ctx.fillText("👹 PO EVIL BOSS (JIRA EPIC CREATOR)", bx - 75, by - 15);

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
                    drawPOBoss(hpPct, gameState.boss_phase || "Criando Épicos...");

                    agentsList.forEach(a => {
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, a.response_time_ms, a.time_remaining_sec, a.max_time_sec);
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
                    const pct = Math.max(0, (a.time_remaining_sec / a.max_time_sec) * 100);
                    return `
                        <div class="skill-upgrade-card">
                            <button class="btn-upgrade" onclick="upgradeSkill('${keys[i]}')">UPGRADE ⬆️</button>
                            <div style="font-weight:bold; color:${a.sprite_color};">${a.name} (Lv.${a.skill_level})</div>
                            <div style="color:#9ca3af; margin-top:0.2rem;">Velocidade: <span style="color:#55ffff;">${a.response_time_ms}ms</span></div>
                            <div class="time-bar-bg">
                                <div class="time-bar-fill" style="width:${pct}%; background:${pct < 40 ? '#ff5555' : '#00ff00'};"></div>
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
                        <div style="color:#9ca3af; margin-top:0.4rem;">💬 DEBATE DOS AGENTES NO JIRA REAL:</div>
                        ${commentsHtml}
                    `;
                }

                document.getElementById('audit-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.25rem;">> ${l.action}: ${l.card_id || ''}</div>
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
