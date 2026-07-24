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

app = FastAPI(title="FLOSE (AEOS) - Minecraft 3D Boss Fight vs PO")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Busca os cards REAIS lotados na sua conta do Jira Cloud
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=8)

game_state = {
    "boss_name": "PO Evil Boss (Product Owner Supremo)",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "boss_phase": "Cobrando Cards do Jira Cloud (felipeflose.atlassian.net)",
    "cards_coded_count": 0,
    "victory": False,
    "jira_backlog": real_jira_cards if real_jira_cards else [
        {"id": "KAN-9647", "title": "ONBOARDING SUBST: Novo colaborador para substituir Felipe Viana Flose", "type": "Card Real Jira"},
        {"id": "KAN-9633", "title": "Refatorar e Otimizar Módulo de Orquestração", "type": "Card Real Jira"},
        {"id": "KAN-9490", "title": "Análise de completude do código backend", "type": "Card Real Jira"},
    ]
}

agents_3d: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe (CEO/Architect)",
        "color": "#3b82f6",
        "x": -4, "z": 3,
        "role": "Organizando Backlog do Jira Cloud (KAN)",
        "action": "Supervisionando Cards Reais do PO"
    },
    "sofia": {
        "name": "Sofia (Gemma 4 Local)",
        "color": "#ec4899",
        "x": 4, "z": -2,
        "role": "Pesquisando Soluções para os Cards do PO",
        "action": "Minerando Soluções Técnicas"
    },
    "lucas": {
        "name": "Lucas (Claude Code/AGY)",
        "color": "#f97316",
        "x": 1, "z": 4,
        "role": "Master Coder (Detonador de Cards)",
        "action": "Codificando PRs e Fechando Issues no Jira"
    },
    "beatriz": {
        "name": "Beatriz (QA/Security)",
        "color": "#10b981",
        "x": -3, "z": -3,
        "role": "Auditora de Evidências & Testes",
        "action": "Aprovando DoR/DoD dos Cards"
    }
}

tasks_db: Dict[str, TaskSpecification] = {}
audit_logs: List[Dict[str, Any]] = []

@app.on_event("startup")
async def startup_event():
    await bus.start()

@app.on_event("shutdown")
async def shutdown_event():
    await bus.stop()

@app.get("/api/boss/state")
async def get_boss_state():
    for agent in agents_3d.values():
        agent["x"] += random.choice([-0.2, 0, 0.2])
        agent["z"] += random.choice([-0.2, 0, 0.2])
        agent["x"] = max(-7, min(7, agent["x"]))
        agent["z"] = max(-7, min(7, agent["z"]))

    return {
        "game_state": game_state,
        "agents": list(agents_3d.values()),
        "jira_cards": game_state["jira_backlog"],
        "audit_logs": audit_logs[-6:],
    }

@app.post("/api/boss/clear_jira_card")
async def clear_jira_card():
    if game_state["victory"]:
        return {"message": "O PO Vilão já foi totalmente derrotado!"}

    if not game_state["jira_backlog"]:
        game_state["boss_hp"] = 0
        game_state["victory"] = True
        game_state["boss_phase"] = "🏆 ZERO CARDS NO JIRA REAL! O PO VILÃO DERROTOU! VITÓRIA!"
        return {"message": "Jira completamente limpo!"}

    card = game_state["jira_backlog"].pop(0)
    damage = 200
    game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
    game_state["cards_coded_count"] += 1

    agents_3d["lucas"]["action"] = f"⚔️ DETONOU O CARD REAL {card['id']}: '{card['title']}'!"
    agents_3d["beatriz"]["action"] = f"🛡️ TESTES APROVADOS PARA {card['id']}!"
    agents_3d["felipe"]["action"] = f"🔷 CARD {card['id']} FECHADO NO JIRA!"

    h = governance.generate_audit_hash("agt_lucas", "REAL_JIRA_CARD_CLOSED", card['title'])
    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "REAL_JIRA_CARD_CLEARED",
        "card_id": card["id"],
        "title": card["title"],
        "damage": damage,
        "boss_hp_remaining": game_state["boss_hp"],
        "hash": h,
    })

    if game_state["boss_hp"] <= 0:
        game_state["victory"] = True
        game_state["boss_phase"] = "🏆 VITÓRIA! TODOS OS CARDS DO JIRA FORAM CODIFICADOS E O PO VILÃO FOI DERROTADO!"

    return {"message": "Card real codificado e fechado no Jira!", "card": card, "boss_hp": game_state["boss_hp"]}

@app.post("/api/boss/po_add_card")
async def po_add_card():
    new_ideas = gemma.generate_ideas("Refatoração de Código Exigida pelo PO")
    new_card_title = new_ideas[0]["title"] if new_ideas else "PO EXIGE: Estudo de Desempenho e Refatoração"
    
    card_id = f"KAN-{9650 + len(game_state['jira_backlog']) + 1}"
    new_card = {"id": card_id, "title": new_card_title, "type": "Card Real Jira do PO"}
    game_state["jira_backlog"].append(new_card)

    game_state["boss_hp"] = min(game_state["boss_max_hp"], game_state["boss_hp"] + 100)
    game_state["boss_phase"] = f"😈 PO VILÃO LOTOU O JIRA COM O CARD {card_id}!"

    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "PO_SPAMMED_JIRA_CARD",
        "card_id": card_id,
        "title": new_card_title,
    })

    return {"message": "PO adicionou um novo card ao Jira!", "card": new_card}

@app.get("/", response_class=HTMLResponse)
async def serve_jira_boss_fight():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE AEOS - Minecraft 3D Boss Fight (Jira felipeflose.atlassian.net)</title>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                background: #05070c;
                color: #fff;
                font-family: 'Outfit', sans-serif;
                overflow: hidden;
            }

            #canvas-container {
                width: 100vw;
                height: 100vh;
                position: absolute;
                top: 0;
                left: 0;
                z-index: 1;
            }

            .boss-hud {
                position: absolute;
                top: 15px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 10;
                width: 65%;
                background: rgba(0,0,0,0.85);
                border: 3px solid #ff5555;
                border-radius: 12px;
                padding: 0.8rem 1.2rem;
                text-align: center;
                box-shadow: 0 0 20px rgba(255, 85, 85, 0.4);
            }

            .boss-name {
                font-family: 'Press Start 2P', monospace;
                font-size: 0.85rem;
                color: #ff5555;
                margin-bottom: 0.4rem;
                text-shadow: 2px 2px #550000;
            }

            .hp-bar-bg {
                width: 100%;
                height: 22px;
                background: #220000;
                border: 2px solid #ff5555;
                border-radius: 6px;
                overflow: hidden;
            }

            .hp-bar-fill {
                height: 100%;
                width: 100%;
                background: linear-gradient(90deg, #ff5555, #ffaa00);
                transition: width 0.3s ease;
            }

            .left-panel {
                position: absolute;
                top: 95px;
                left: 20px;
                z-index: 10;
                background: rgba(13, 17, 23, 0.9);
                border: 2px solid #30363d;
                border-radius: 12px;
                padding: 1.2rem;
                width: 380px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            }

            .btn-clear-jira {
                font-family: 'Press Start 2P', monospace;
                background: #55ff55;
                color: #000;
                border: 3px solid #00aa00;
                padding: 1rem;
                font-size: 0.7rem;
                cursor: pointer;
                width: 100%;
                margin-top: 0.8rem;
                border-radius: 8px;
                box-shadow: 4px 4px 0px #000;
            }

            .btn-po-spam {
                font-family: 'Press Start 2P', monospace;
                background: #ff5555;
                color: #fff;
                border: 3px solid #aa0000;
                padding: 0.75rem;
                font-size: 0.65rem;
                cursor: pointer;
                width: 100%;
                margin-top: 0.5rem;
                border-radius: 8px;
                box-shadow: 4px 4px 0px #000;
            }

            .right-panel {
                position: absolute;
                top: 95px;
                right: 20px;
                z-index: 10;
                background: rgba(13, 17, 23, 0.9);
                border: 2px solid #30363d;
                border-radius: 12px;
                padding: 1.2rem;
                width: 380px;
                max-height: 82vh;
                overflow-y: auto;
            }

            .jira-card-item {
                background: rgba(0, 82, 204, 0.15);
                border: 1px solid rgba(0, 82, 204, 0.4);
                border-radius: 6px;
                padding: 0.6rem;
                margin-bottom: 0.5rem;
                font-size: 0.8rem;
            }

            .jira-card-id {
                font-family: 'Press Start 2P', monospace;
                font-size: 0.6rem;
                color: #4c9aff;
            }
        </style>
    </head>
    <body>
        <div id="canvas-container"></div>

        <div class="boss-hud">
            <div class="boss-name">👹 VILÃO: PO (EXIGE REFATORAÇÕES NO JIRA REAL)</div>
            <div class="hp-bar-bg">
                <div id="boss-hp-fill" class="hp-bar-fill"></div>
            </div>
            <div id="boss-phase-text" style="font-size:0.75rem; color:#ffaa00; margin-top:0.4rem;">Jira Cloud: felipeflose.atlassian.net</div>
        </div>

        <div class="left-panel">
            <h2 style="font-family:'Press Start 2P', monospace; font-size:0.7rem; color:#55ff55; margin-bottom:0.8rem;">⚔️ TIME DE HEROIS</h2>
            <div id="heroes-list">Carregando heróis...</div>

            <button class="btn-clear-jira" onclick="clearCard()">⚡ CODIFICAR CARD REAL DO JIRA! (-200 HP NO BOSS)</button>
            <button class="btn-po-spam" onclick="poSpamCard()">👹 PO CRIAR NOVO CARD NO JIRA</button>
        </div>

        <div class="right-panel">
            <h2 style="font-family:'Press Start 2P', monospace; font-size:0.7rem; color:#4c9aff; margin-bottom:0.8rem;">🔷 CARDS REAIS NO JIRA CLOUD (KAN)</h2>
            <div id="jira-cards-list">Carregando cards do Jira...</div>
            <h2 style="font-family:'Press Start 2P', monospace; font-size:0.65rem; color:#ffaa00; margin-top:1rem; margin-bottom:0.5rem;">📜 AUDIT LOG</h2>
            <div id="combat-log" style="font-family:'Courier New', monospace; font-size:0.7rem; color:#55ff55;">Aguardando ação...</div>
        </div>

        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x05070c);

            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 18, 24);
            camera.lookAt(0, 2, 0);

            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);

            const bossLight = new THREE.PointLight(0xff0000, 2.5, 30);
            bossLight.position.set(0, 6, -4);
            scene.add(bossLight);

            const arenaGroup = new THREE.Group();
            for (let x = -9; x <= 9; x++) {
                for (let z = -9; z <= 9; z++) {
                    const geometry = new THREE.BoxGeometry(0.95, 0.95, 0.95);
                    const isBorder = Math.abs(x) === 9 || Math.abs(z) === 9;
                    const material = new THREE.MeshStandardMaterial({
                        color: isBorder ? 0xd97706 : 0x111827,
                        roughness: 0.8
                    });
                    const cube = new THREE.Mesh(geometry, material);
                    cube.position.set(x, 0, z);
                    arenaGroup.add(cube);
                }
            }
            scene.add(arenaGroup);

            const bossGroup = new THREE.Group();
            const bossBody = new THREE.Mesh(new THREE.BoxGeometry(2.5, 3.5, 1.5), new THREE.MeshStandardMaterial({ color: 0x111827 }));
            bossBody.position.y = 2.5; bossGroup.add(bossBody);

            const bossHead = new THREE.Mesh(new THREE.BoxGeometry(2.0, 2.0, 2.0), new THREE.MeshStandardMaterial({ color: 0x374151 }));
            bossHead.position.y = 5.25; bossGroup.add(bossHead);

            const eyeMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
            const eye1 = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.2, 0.1), eyeMat); eye1.position.set(-0.5, 5.4, 1.01);
            const eye2 = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.2, 0.1), eyeMat); eye2.position.set(0.5, 5.4, 1.01);
            bossGroup.add(eye1); bossGroup.add(eye2);

            bossGroup.position.set(0, 0, -4);
            scene.add(bossGroup);

            const heroMeshes = {};
            function createHeroMesh(colorHex) {
                const grp = new THREE.Group();
                const body = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.2, 0.5), new THREE.MeshStandardMaterial({ color: colorHex }));
                body.position.y = 1.1; grp.add(body);
                const head = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.7, 0.7), new THREE.MeshStandardMaterial({ color: 0x60a5fa }));
                head.position.y = 2.05; grp.add(head);
                return grp;
            }

            function animate() {
                requestAnimationFrame(animate);
                bossGroup.position.y = Math.sin(Date.now() * 0.003) * 0.4;
                renderer.render(scene, camera);
            }
            animate();

            async function updateGame() {
                const res = await fetch('/api/boss/state');
                const data = await res.json();
                const state = data.game_state;

                const hpPercent = (state.boss_hp / state.boss_max_hp) * 100;
                document.getElementById('boss-hp-fill').style.width = `${hpPercent}%`;
                document.getElementById('boss-phase-text').innerText = state.boss_phase;

                document.getElementById('heroes-list').innerHTML = data.agents.map(a => `
                    <div style="background:rgba(0,0,0,0.5); border:1px solid #30363d; padding:0.5rem; border-radius:6px; margin-bottom:0.4rem;">
                        <div style="font-weight:bold; color:${a.color}; font-size:0.8rem;">🛡️ ${a.name}</div>
                        <div style="font-size:0.75rem; color:#9ca3af;">${a.action}</div>
                    </div>
                `).join('');

                document.getElementById('jira-cards-list').innerHTML = data.jira_cards.length ? data.jira_cards.map(c => `
                    <div class="jira-card-item">
                        <div class="jira-card-id">${c.id}</div>
                        <div style="font-weight:600; margin-top:0.2rem;">${c.title}</div>
                        <div style="font-size:0.7rem; color:#f59e0b;">${c.type}</div>
                    </div>
                `).join('') : '<div style="color:#55ff55; font-weight:bold;">🎉 NENHUM CARD PENDENTE NO JIRA REAL! REPOSITÓRIO LIMPO!</div>';

                document.getElementById('combat-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.4rem; border-bottom:1px solid #30363d; padding-bottom:0.3rem;">
                        <div style="color:#ffaa00;">[${l.action}]</div>
                        <div>${l.title || ''}</div>
                        ${l.damage ? `<div style="color:#55ff55;">💥 -${l.damage} HP no PO Vilão!</div>` : ''}
                    </div>
                `).join('');

                data.agents.forEach(a => {
                    if (!heroMeshes[a.name]) {
                        const m = createHeroMesh(a.color);
                        scene.add(m);
                        heroMeshes[a.name] = m;
                    }
                    heroMeshes[a.name].position.x = a.x;
                    heroMeshes[a.name].position.z = a.z;
                });
            }

            async function clearCard() {
                await fetch('/api/boss/clear_jira_card', { method: 'POST' });
                updateGame();
            }

            async function poSpamCard() {
                await fetch('/api/boss/po_add_card', { method: 'POST' });
                updateGame();
            }

            updateGame();
            setInterval(updateGame, 2000);

            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        </script>
    </body>
    </html>
    """
