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

app = FastAPI(title="FLOSE (AEOS) - 2D Pixel Agents RPG Boss Fight vs PO")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Busca os cards REAIS do Jira Cloud (felipeflose.atlassian.net)
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=8)

game_state = {
    "boss_name": "PO EVIL BOSS",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "boss_phase": "Exigindo Refatorações no Jira Cloud",
    "cards_coded_count": 0,
    "victory": False,
    "jira_backlog": real_jira_cards if real_jira_cards else [
        {"id": "KAN-9647", "title": "ONBOARDING SUBST: Novo colaborador para substituir Felipe Viana Flose", "type": "Card Real Jira"},
        {"id": "KAN-9633", "title": "Refatorar e Otimizar Módulo de Orquestração", "type": "Card Real Jira"},
        {"id": "KAN-9490", "title": "Análise de completude do código backend", "type": "Card Real Jira"},
    ]
}

# Pixel Agents com posições na tela 2D Canvas (Pixel Art Style)
pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe",
        "class": "Pixel Architect Leader",
        "sprite_color": "#3b82f6",
        "x": 80, "y": 280,
        "action": "Supervisionando o Backlog",
        "hp": 100
    },
    "sofia": {
        "name": "Sofia",
        "class": "Gemma 4 Idea Miner",
        "sprite_color": "#ec4899",
        "x": 220, "y": 240,
        "action": "Pesquisando Soluções Pixel",
        "hp": 98
    },
    "lucas": {
        "name": "Lucas",
        "class": "Claude Code Coder",
        "sprite_color": "#f97316",
        "x": 360, "y": 280,
        "action": "Codificando PRs Super Rápido",
        "hp": 99
    },
    "beatriz": {
        "name": "Beatriz",
        "class": "QA & Security Shield",
        "sprite_color": "#10b981",
        "x": 500, "y": 240,
        "action": "Auditando Testes e Evidências",
        "hp": 97
    }
}

audit_logs: List[Dict[str, Any]] = []

@app.on_event("startup")
async def startup_event():
    await bus.start()

@app.on_event("shutdown")
async def shutdown_event():
    await bus.stop()

@app.get("/api/boss/state")
async def get_boss_state():
    # Animação suave dos Pixel Agents no canvas 2D
    for agent in pixel_agents.values():
        agent["x"] += random.choice([-2, 0, 2])
        agent["y"] += random.choice([-2, 0, 2])
        agent["x"] = max(50, min(550, agent["x"]))
        agent["y"] = max(200, min(320, agent["y"]))

    return {
        "game_state": game_state,
        "pixel_agents": list(pixel_agents.values()),
        "jira_cards": game_state["jira_backlog"],
        "audit_logs": audit_logs[-6:],
    }

@app.post("/api/boss/clear_jira_card")
async def clear_jira_card():
    if game_state["victory"]:
        return {"message": "O PO Vilão já foi derrotado!"}

    if not game_state["jira_backlog"]:
        game_state["boss_hp"] = 0
        game_state["victory"] = True
        game_state["boss_phase"] = "🏆 ZERO CARDS NO JIRA REAL! VITÓRIA DOS PIXEL AGENTES!"
        return {"message": "Jira completamente limpo!"}

    card = game_state["jira_backlog"].pop(0)
    damage = 200
    game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
    game_state["cards_coded_count"] += 1

    pixel_agents["lucas"]["action"] = f"⚔️ PIXEL ATTACK! Codificou {card['id']}!"
    pixel_agents["beatriz"]["action"] = f"🛡️ TESTES APROVADOS PARA {card['id']}!"
    pixel_agents["felipe"]["action"] = f"🔷 CARD {card['id']} FECHADO NO JIRA!"

    h = governance.generate_audit_hash("agt_lucas", "PIXEL_CARD_CLOSED", card['title'])
    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "PIXEL_AGENT_CLEARED_CARD",
        "card_id": card["id"],
        "title": card["title"],
        "damage": damage,
        "boss_hp_remaining": game_state["boss_hp"],
        "hash": h,
    })

    if game_state["boss_hp"] <= 0:
        game_state["victory"] = True
        game_state["boss_phase"] = "🏆 VITÓRIA! TODOS OS CARDS FORAM CODIFICADOS E O PO VILÃO CAIU!"

    return {"message": "Card codificado pelos Pixel Agentes!", "card": card, "boss_hp": game_state["boss_hp"]}

@app.post("/api/boss/po_add_card")
async def po_add_card():
    new_ideas = gemma.generate_ideas("Refatoração Pixel Exigida pelo PO")
    new_card_title = new_ideas[0]["title"] if new_ideas else "PO EXIGE: Otimizar Sprites Pixel em Assembly"
    
    card_id = f"KAN-{9650 + len(game_state['jira_backlog']) + 1}"
    new_card = {"id": card_id, "title": new_card_title, "type": "Card Real Jira do PO"}
    game_state["jira_backlog"].append(new_card)

    game_state["boss_hp"] = min(game_state["boss_max_hp"], game_state["boss_hp"] + 100)
    game_state["boss_phase"] = f"😈 PO VILÃO ADICIONOU CARD {card_id}!"

    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "PO_SPAMMED_JIRA_CARD",
        "card_id": card_id,
        "title": new_card_title,
    })

    return {"message": "PO adicionou um novo card ao Jira!", "card": new_card}

@app.get("/", response_class=HTMLResponse)
async def serve_pixel_agents_game():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE AEOS - Pixel Agents 16-Bit RPG vs PO Boss</title>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                background: #0d0e15;
                color: #fff;
                font-family: 'Press Start 2P', monospace;
                overflow: hidden;
            }

            /* Container Principal do Jogo Pixel Art */
            #game-container {
                display: flex;
                width: 100vw;
                height: 100vh;
            }

            /* Canvas da Arena Pixel Art */
            #pixel-canvas {
                background: #181926;
                border-right: 4px solid #3b3d54;
                image-rendering: pixelated;
                image-rendering: crisp-edges;
            }

            /* Side Panel Direita (Jira Cards & Controles) */
            .side-panel {
                width: 420px;
                background: #11121d;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border-left: 4px solid #3b3d54;
                overflow-y: auto;
            }

            .hud-title {
                font-size: 0.8rem;
                color: #55ff55;
                margin-bottom: 0.8rem;
                text-shadow: 2px 2px #00aa00;
            }

            .btn-pixel-attack {
                background: #55ff55;
                color: #000;
                border: 3px solid #00aa00;
                padding: 1rem;
                font-size: 0.65rem;
                cursor: pointer;
                width: 100%;
                margin-bottom: 0.6rem;
                box-shadow: 4px 4px 0px #000;
                font-family: 'Press Start 2P', monospace;
            }

            .btn-pixel-attack:active {
                transform: translate(2px, 2px);
                box-shadow: 2px 2px 0px #000;
            }

            .btn-po-attack {
                background: #ff5555;
                color: #fff;
                border: 3px solid #aa0000;
                padding: 0.75rem;
                font-size: 0.6rem;
                cursor: pointer;
                width: 100%;
                margin-bottom: 1rem;
                box-shadow: 4px 4px 0px #000;
                font-family: 'Press Start 2P', monospace;
            }

            .jira-card {
                background: rgba(59, 130, 246, 0.15);
                border: 2px solid #3b82f6;
                border-radius: 4px;
                padding: 0.6rem;
                margin-bottom: 0.5rem;
                font-size: 0.55rem;
                line-height: 1.4;
            }

            .card-id { color: #60a5fa; font-weight: bold; }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>

            <div class="side-panel">
                <div>
                    <div class="hud-title">👾 PIXEL AGENTS vs PO BOSS</div>
                    <div style="font-size: 0.55rem; color: #9ca3af; margin-bottom: 1rem;">Conta: felipeflose.atlassian.net</div>

                    <button class="btn-pixel-attack" onclick="clearCard()">⚡ CODIFICAR CARD (-200 HP PO)</button>
                    <button class="btn-po-attack" onclick="poAttack()">👹 PO LOTAR JIRA COM NOVO CARD</button>

                    <div style="font-size: 0.65rem; color: #ffaa00; margin-top: 1rem; margin-bottom: 0.6rem;">🔷 CARDS NO JIRA CLOUD</div>
                    <div id="cards-list">Carregando cards...</div>
                </div>

                <div>
                    <div style="font-size: 0.6rem; color: #55ff55; margin-bottom: 0.5rem;">📜 AUDIT LOG HASHS</div>
                    <div id="audit-log" style="font-size: 0.5rem; color: #9ca3af; max-height: 120px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('pixel-canvas');
            const ctx = canvas.getContext('2d');

            function resizeCanvas() {
                canvas.width = window.innerWidth - 420;
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];

            // Desenhar Sprite Pixel Art 16-Bit dos Agentes
            function drawPixelSprite(x, y, color, name, role) {
                // Corpo do Agente Pixel (16x24 pixels)
                ctx.fillStyle = color;
                ctx.fillRect(x, y + 10, 24, 20);

                // Cabeça Pixel
                ctx.fillStyle = "#ffcc99";
                ctx.fillRect(x + 4, y, 16, 14);

                // Olhos Pixel
                ctx.fillStyle = "#000";
                ctx.fillRect(x + 7, y + 4, 3, 3);
                ctx.fillRect(x + 14, y + 4, 3, 3);

                // Nome do Agente por cima do Sprite
                ctx.font = '8px "Press Start 2P"';
                ctx.fillStyle = color;
                ctx.fillText(name, x - 5, y - 8);

                // Barra de Vida Mini
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(x - 4, y - 4, 30, 3);
                ctx.fillStyle = "#00ff00";
                ctx.fillRect(x - 4, y - 4, 28, 3);
            }

            // Desenhar PO EVIL BOSS Giant Pixel Sprite
            function drawPOBoss(hpPercent, phaseText) {
                const bx = canvas.width / 2 - 40;
                const by = 40;

                // Corpo do PO Vilão (Terno Escuro)
                ctx.fillStyle = "#1e1e2e";
                ctx.fillRect(bx, by + 30, 80, 70);

                // Gravata Vermelha
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 36, by + 35, 8, 35);

                // Cabeça Gigante do Boss
                ctx.fillStyle = "#313244";
                ctx.fillRect(bx + 10, by, 60, 40);

                // Olhos de Laser Vermelhos
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 20, by + 12, 12, 8);
                ctx.fillRect(bx + 48, by + 12, 12, 8);

                // Nome do Boss
                ctx.font = '12px "Press Start 2P"';
                ctx.fillStyle = "#ff5555";
                ctx.fillText("👹 PO EVIL BOSS", bx - 30, by - 15);

                // Barra de Vida Gigante do Boss
                ctx.fillStyle = "#440000";
                ctx.fillRect(canvas.width / 2 - 150, 15, 300, 16);
                ctx.fillStyle = "#ff3333";
                ctx.fillRect(canvas.width / 2 - 150, 15, (300 * hpPercent) / 100, 16);
                ctx.strokeStyle = "#ffffff";
                ctx.strokeRect(canvas.width / 2 - 150, 15, 300, 16);

                // Texto de Status da Fase
                ctx.font = '8px "Press Start 2P"';
                ctx.fillStyle = "#ffaa00";
                ctx.fillText(phaseText, canvas.width / 2 - 140, 42);
            }

            // Loop de Renderização do Canvas 2D
            function render() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Desenhar chão da Arena Pixel (Grid 16-bit)
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
                    drawPOBoss(hpPct, gameState.boss_phase || "Carregando PO...");

                    // Desenhar cada Pixel Agente (Felipe, Sofia, Lucas, Beatriz)
                    agentsList.forEach(a => {
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, a.class);
                    });
                }

                requestAnimationFrame(render);
            }
            render();

            // Atualizar Estado do Jogo via API REST
            async function updateState() {
                const res = await fetch('/api/boss/state');
                const data = await res.json();
                gameState = data.game_state;
                agentsList = data.pixel_agents;

                // Atualizar Cards no Painel
                document.getElementById('cards-list').innerHTML = data.jira_cards.length ? data.jira_cards.map(c => `
                    <div class="jira-card">
                        <div class="card-id">${c.id}</div>
                        <div>${c.title}</div>
                    </div>
                `).join('') : '<div style="color:#55ff55; font-size:0.6rem;">🎉 JIRA LIMPO! VITORIA!</div>';

                // Audit Log
                document.getElementById('audit-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.3rem;">> ${l.action}: ${l.title || ''}</div>
                `).join('');
            }

            async function clearCard() {
                await fetch('/api/boss/clear_jira_card', { method: 'POST' });
                updateState();
            }

            async function poAttack() {
                await fetch('/api/boss/po_add_card', { method: 'POST' });
                updateState();
            }

            updateState();
            setInterval(updateState, 2000);
        </script>
    </body>
    </html>
    """
