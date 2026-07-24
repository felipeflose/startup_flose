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

app = FastAPI(title="FLOSE (AEOS) - Minecraft 3D Boss Fight vs PO Evil Boss")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Estado da Batalha contra o PO Vilão (Boss HP = 1000)
game_state = {
    "boss_name": "PO Evil Boss (Product Owner Supremo)",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "boss_phase": "Analisando Código Atual & Gerando Refatorações Impossíveis",
    "team_xp": 0,
    "victory": False,
    "attack_cards": []
}

agents_3d: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe (CEO/Architect)",
        "color": "#3b82f6",
        "x": -4, "z": 3,
        "role": "Líder de Defesa & Orquestrador",
        "dps": 45,
        "action": "Estratégia de Defesa contra Cards do PO"
    },
    "sofia": {
        "name": "Sofia (Gemma 4 Local)",
        "color": "#ec4899",
        "x": 4, "z": -2,
        "role": "Engenheira de Ideias Anti-Refatoração",
        "dps": 50,
        "action": "Pesquisando Tecnologias para Contra-Atacar o PO"
    },
    "lucas": {
        "name": "Lucas (Claude Code/AGY)",
        "color": "#f97316",
        "x": 1, "z": 4,
        "role": "Master Coder (Codifica Cards Super Rápido)",
        "dps": 65,
        "action": "Codificando PRs para Zerar a Fila de Cards"
    },
    "beatriz": {
        "name": "Beatriz (QA/Security)",
        "color": "#10b981",
        "x": -3, "z": -3,
        "role": "Escudo de Testes & Anti-Alucinação",
        "dps": 40,
        "action": "Auditando Testes e Destruindo Cards Inválidos"
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
    # Movimentação 3D na arena do Boss
    for agent in agents_3d.values():
        agent["x"] += random.choice([-0.3, 0, 0.3])
        agent["z"] += random.choice([-0.3, 0, 0.3])
        agent["x"] = max(-7, min(7, agent["x"]))
        agent["z"] = max(-7, min(7, agent["z"]))

    return {
        "game_state": game_state,
        "agents": list(agents_3d.values()),
        "cards_pending": game_state["attack_cards"],
        "tasks": list(tasks_db.values()),
        "audit_logs": audit_logs[-5:],
    }

@app.post("/api/boss/po_attack")
async def po_boss_attack():
    """O PO Vilão analisa o código e ataca a equipe lançando novos Cards/Refatorações difíceis!"""
    if game_state["victory"]:
        return {"message": "O PO Vilão já foi derrotado!"}

    # Ataque do PO via Gemma 4 Local (Simula o PO pesquisando melhorias e cobrando o time)
    attack_ideas = gemma.generate_ideas("Refatoração Crítica de Arquitetura e Estudos de Performance")
    new_card = attack_ideas[0] if attack_ideas else {
        "title": "CARD VILÃO: Refatorar Todo o Sistema para Microserviços Async",
        "summary": "O PO achou o código atual lento e exige estudo completo!",
        "jira_priority": "Highest"
    }

    game_state["attack_cards"].append(new_card)
    game_state["boss_phase"] = f"🔥 ATAQUE DO PO: Lançou '{new_card['title']}'!"
    
    # Registra o Card do PO no Jira
    j_res = jira.create_issue(
        project_key="FLO",
        summary=f"[PO-BOSS-ATTACK] {new_card['title']}",
        description=f"Card lançado pelo PO Vilão! Exige refatoração: {new_card['summary']}"
    )

    audit_logs.append({
        "event_id": f"evt_{len(audit_logs)+1}",
        "action": "PO_BOSS_ATTACKED",
        "title": new_card["title"],
        "jira": j_res.get("key", "FLO-PO-BOSS"),
    })

    return {"message": "Ataque do PO executado!", "card": new_card}

@app.post("/api/boss/code_and_fight")
async def code_and_fight_boss():
    """O time (Felipe, Sofia, Lucas e Beatriz) pega os cards, codifica e ataca o PO Vilão para ganhar a partida!"""
    if game_state["victory"]:
        return {"message": "Vitória já conquistada!"}

    if not game_state["attack_cards"]:
        # Se não há cards, o time ataca diretamente
        damage = 150
        game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
    else:
        # Pega o card da fila e codifica
        card = game_state["attack_cards"].pop(0)
        
        # Decompõe e codifica o card do PO
        created_tasks = planner.decompose_goal("BOSS_FIGHT", card["title"], [
            f"Felipe & Sofia: Estudar refatoração exótica do PO",
            f"Lucas: Codificar a solução em recorde de tempo via Claude Code & AGY",
            f"Beatriz: Aplicar suíte de testes e fechar o card no Jira"
        ])
        
        for task in created_tasks:
            tasks_db[task.task_id] = task
        
        # Dano massivo no Boss ao codificar o card!
        damage = 250
        game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
        game_state["team_xp"] += 100

        # Atualiza status dos heróis
        agents_3d["lucas"]["action"] = f"⚔️ DESTRUIU O CARD '{card['title']}' CODIFICANDO TUDO!"
        agents_3d["beatriz"]["action"] = "🛡️ TESTES APROVADOS! EVIDÊNCIA ANEXADA!"
        agents_3d["felipe"]["action"] = "🎯 CARD FECHADO NO JIRA! BOSS SOFREU CRITICAL HIT!"

        audit_logs.append({
            "event_id": f"evt_{len(audit_logs)+1}",
            "action": "TEAM_CODED_CARD_AND_HIT_BOSS",
            "card_cleared": card["title"],
            "damage_dealt": damage,
            "boss_hp_remaining": game_state["boss_hp"]
        })

    if game_state["boss_hp"] <= 0:
        game_state["victory"] = True
        game_state["boss_phase"] = "🏆 VITÓRIA ABSOLUTA! O PO VILÃO FOI DERROTADO PELO TIME DE ENGENHARIA!"

    return {
        "boss_hp": game_state["boss_hp"],
        "damage_dealt": damage,
        "victory": game_state["victory"]
    }

@app.get("/", response_class=HTMLResponse)
async def serve_boss_fight_game():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE AEOS - Minecraft 3D Boss Fight vs PO</title>
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

            /* Boss Health Bar HUD Top */
            .boss-hud {
                position: absolute;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 10;
                width: 60%;
                background: rgba(0,0,0,0.85);
                border: 3px solid #ff5555;
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                box-shadow: 0 0 20px rgba(255, 85, 85, 0.4);
            }

            .boss-name {
                font-family: 'Press Start 2P', monospace;
                font-size: 0.9rem;
                color: #ff5555;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px #550000;
            }

            .hp-bar-bg {
                width: 100%;
                height: 24px;
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

            /* Left Actions Menu */
            .left-panel {
                position: absolute;
                top: 100px;
                left: 20px;
                z-index: 10;
                background: rgba(13, 17, 23, 0.9);
                border: 2px solid #30363d;
                border-radius: 12px;
                padding: 1.2rem;
                width: 380px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            }

            .btn-code {
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

            .btn-po-attack {
                font-family: 'Press Start 2P', monospace;
                background: #ff5555;
                color: #fff;
                border: 3px solid #aa0000;
                padding: 0.8rem;
                font-size: 0.65rem;
                cursor: pointer;
                width: 100%;
                margin-top: 0.5rem;
                border-radius: 8px;
                box-shadow: 4px 4px 0px #000;
            }

            /* Right Logs */
            .right-panel {
                position: absolute;
                top: 100px;
                right: 20px;
                z-index: 10;
                background: rgba(13, 17, 23, 0.9);
                border: 2px solid #30363d;
                border-radius: 12px;
                padding: 1.2rem;
                width: 360px;
                max-height: 80vh;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <div id="canvas-container"></div>

        <!-- Boss HUD -->
        <div class="boss-hud">
            <div class="boss-name">👹 VILÃO: PO (PRODUCT OWNER SUPREMO)</div>
            <div class="hp-bar-bg">
                <div id="boss-hp-fill" class="hp-bar-fill"></div>
            </div>
            <div id="boss-phase-text" style="font-size:0.8rem; color:#ffaa00; margin-top:0.4rem;">Fase: Cobrando Refatoração & Estudos</div>
        </div>

        <!-- Left Controls -->
        <div class="left-panel">
            <h2 style="font-family:'Press Start 2P', monospace; font-size:0.75rem; color:#55ff55; margin-bottom:0.8rem;">⚔️ HERÓIS DA ENGENHARIA</h2>
            <div id="heroes-list">Carregando heróis...</div>

            <button class="btn-code" onclick="codeAndFight()">💻 PEGAR CARD DO PO & CODIFICAR! (ATACAR BOSS)</button>
            <button class="btn-po-attack" onclick="poAttack()">👹 PO LANÇAR NOVO CARD / ESTUDO</button>
        </div>

        <!-- Right Logs -->
        <div class="right-panel">
            <h2 style="font-family:'Press Start 2P', monospace; font-size:0.75rem; color:#ffaa00; margin-bottom:0.8rem;">📜 AUDIT LOG & COMBATE</h2>
            <div id="cards-pending-container" style="margin-bottom:1rem;"></div>
            <div id="combat-log" style="font-family:'Courier New', monospace; font-size:0.75rem; color:#55ff55;">Batalha iniciada!</div>
        </div>

        <script>
            // Setup Three.js Boss Arena 3D
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

            // Arena Lighting (Reddish Boss Atmosphere)
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);

            const bossLight = new THREE.PointLight(0xff0000, 2, 30);
            bossLight.position.set(0, 6, 0);
            scene.add(bossLight);

            // Nether / Lava Voxel Arena Floor
            const arenaGroup = new THREE.Group();
            for (let x = -9; x <= 9; x++) {
                for (let z = -9; z <= 9; z++) {
                    const geometry = new THREE.BoxGeometry(0.95, 0.95, 0.95);
                    const isBorder = Math.abs(x) === 9 || Math.abs(z) === 9;
                    const material = new THREE.MeshStandardMaterial({
                        color: isBorder ? 0xff3300 : 0x111827,
                        emissive: isBorder ? 0x990000 : 0x000000,
                        roughness: 0.8
                    });
                    const cube = new THREE.Mesh(geometry, material);
                    cube.position.set(x, 0, z);
                    arenaGroup.add(cube);
                }
            }
            scene.add(arenaGroup);

            // CREATE PO EVIL BOSS (Giant 3D Character with Glowing Red Eyes & Suit)
            const bossGroup = new THREE.Group();
            
            // Giant Body
            const bossBodyGeo = new THREE.BoxGeometry(2.5, 3.5, 1.5);
            const bossBodyMat = new THREE.MeshStandardMaterial({ color: 0x1f2937 }); // Dark suit
            const bossBody = new THREE.Mesh(bossBodyGeo, bossBodyMat);
            bossBody.position.y = 2.5;
            bossGroup.add(bossBody);

            // Giant Head
            const bossHeadGeo = new THREE.BoxGeometry(2.0, 2.0, 2.0);
            const bossHeadMat = new THREE.MeshStandardMaterial({ color: 0x374151 });
            const bossHead = new THREE.Mesh(bossHeadGeo, bossHeadMat);
            bossHead.position.y = 5.25;
            bossGroup.add(bossHead);

            // Glowing Red Eyes
            const eyeGeo = new THREE.BoxGeometry(0.4, 0.2, 0.1);
            const eyeMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
            const eyeLeft = new THREE.Mesh(eyeGeo, eyeMat);
            eyeLeft.position.set(-0.5, 5.4, 1.01);
            const eyeRight = new THREE.Mesh(eyeGeo, eyeMat);
            eyeRight.position.set(0.5, 5.4, 1.01);
            bossGroup.add(eyeLeft);
            bossGroup.add(eyeRight);

            // Giant Clipboard (Attack Tool)
            const boardGeo = new THREE.BoxGeometry(1.5, 2.0, 0.2);
            const boardMat = new THREE.MeshStandardMaterial({ color: 0xb91c1c, emissive: 0x7f1d1d });
            const board = new THREE.Mesh(boardGeo, boardMat);
            board.position.set(1.8, 3.5, 0.5);
            bossGroup.add(board);

            bossGroup.position.set(0, 0, -4);
            scene.add(bossGroup);

            // Hero Avatars (Felipe, Sofia, Lucas, Beatriz)
            const heroMeshes = {};

            function createHero3D(colorHex) {
                const group = new THREE.Group();
                const bodyGeo = new THREE.BoxGeometry(0.8, 1.2, 0.5);
                const bodyMat = new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.3 });
                const body = new THREE.Mesh(bodyGeo, bodyMat);
                body.position.y = 1.1;
                group.add(body);

                const headGeo = new THREE.BoxGeometry(0.7, 0.7, 0.7);
                const headMat = new THREE.MeshStandardMaterial({ color: 0x60a5fa }); // Diamond helmet look
                const head = new THREE.Mesh(headGeo, headMat);
                head.position.y = 2.05;
                group.add(head);

                return group;
            }

            function animate() {
                requestAnimationFrame(animate);
                
                // PO Boss Levitation & Float animation
                bossGroup.position.y = Math.sin(Date.now() * 0.003) * 0.4;
                bossHead.rotation.y = Math.sin(Date.now() * 0.002) * 0.2;

                renderer.render(scene, camera);
            }
            animate();

            async function updateGame() {
                const res = await fetch('/api/boss/state');
                const data = await res.json();
                const state = data.game_state;

                // Boss HP Bar
                const hpPercent = (state.boss_hp / state.boss_max_hp) * 100;
                document.getElementById('boss-hp-fill').style.width = `${hpPercent}%`;
                document.getElementById('boss-phase-text').innerText = state.boss_phase;

                // Heroes List
                document.getElementById('heroes-list').innerHTML = data.agents.map(a => `
                    <div style="background:rgba(0,0,0,0.5); border:1px solid #30363d; padding:0.6rem; border-radius:6px; margin-bottom:0.4rem;">
                        <div style="font-weight:bold; color:${a.color};">🛡️ ${a.name}</div>
                        <div style="font-size:0.75rem; color:#9ca3af;">${a.action}</div>
                    </div>
                `).join('');

                // Cards Pending
                document.getElementById('cards-pending-container').innerHTML = data.cards_pending.length ? `
                    <div style="background:rgba(185,28,28,0.2); border:1px solid #b91c1c; padding:0.6rem; border-radius:6px;">
                        <div style="color:#ff5555; font-size:0.75rem; font-weight:bold;">📋 CARDS DO PO NA FILA: ${data.cards_pending.length}</div>
                        <div style="font-size:0.7rem; color:#fca5a5;">Topo: ${data.cards_pending[0].title}</div>
                    </div>
                ` : '<div style="color:#55ff55; font-size:0.75rem;">✅ Nenhum card pendente! O PO está sem ataques!</div>';

                // Combat Log
                document.getElementById('combat-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.5rem; border-bottom:1px solid #30363d; padding-bottom:0.3rem;">
                        <div style="color:#ffaa00;">[${l.action}]</div>
                        <div>${l.title || l.card_cleared || ''}</div>
                        ${l.damage_dealt ? `<div style="color:#55ff55;">💥 Dano no PO: -${l.damage_dealt} HP</div>` : ''}
                    </div>
                `).join('');

                // Update 3D Positions
                data.agents.forEach(a => {
                    if (!heroMeshes[a.name]) {
                        const mesh = createHero3D(a.color);
                        scene.add(mesh);
                        heroMeshes[a.name] = mesh;
                    }
                    heroMeshes[a.name].position.x = a.x;
                    heroMeshes[a.name].position.z = a.z;
                });
            }

            async function codeAndFight() {
                await fetch('/api/boss/code_and_fight', { method: 'POST' });
                updateGame();
            }

            async function poAttack() {
                await fetch('/api/boss/po_attack', { method: 'POST' });
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
