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

app = FastAPI(title="FLOSE (AEOS) - Interactive Minecraft 3D Agent Simulator")

# Core System Instances
bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Agentes com posições 3D no mundo Voxel Minecraft
agents_3d: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "id": "agt_felipe",
        "name": "Felipe",
        "role": "CEO & Architect Leader",
        "color": "#3b82f6",
        "x": -4, "y": 1, "z": 2,
        "action": "Supervisionando a Vila FLOSE",
        "hp": 100,
        "holding": "Diamond Sword"
    },
    "sofia": {
        "id": "agt_sofia",
        "name": "Sofia",
        "role": "Gemma 4 Local Idea Engine",
        "color": "#ec4899",
        "x": 4, "y": 1, "z": -3,
        "action": "Minerando Blocos de Ideias",
        "hp": 98,
        "holding": "Enchanted Pickaxe"
    },
    "lucas": {
        "id": "agt_lucas",
        "name": "Lucas",
        "role": "Claude Code & AGY Master Coder",
        "color": "#f97316",
        "x": 0, "y": 1, "z": 4,
        "action": "Construindo Estrutura de Código Python",
        "hp": 99,
        "holding": "Crafting Table"
    },
    "beatriz": {
        "id": "agt_beatriz",
        "name": "Beatriz",
        "role": "QA & Security Guardian",
        "color": "#10b981",
        "x": -2, "y": 1, "z": -4,
        "action": "Auditando Redstone Hashes & Testes",
        "hp": 97,
        "holding": "Redstone Torch"
    }
}

tasks_db: Dict[str, TaskSpecification] = {}
audit_logs: List[Dict[str, Any]] = []
ideas_db: List[Dict[str, Any]] = []

@app.on_event("startup")
async def startup_event():
    await bus.start()

@app.on_event("shutdown")
async def shutdown_event():
    await bus.stop()

class IdeaGenerateRequest(BaseModel):
    domain_prompt: str = "Inovação Multiagente 3D"
    sync_jira: bool = True

@app.get("/api/world/state")
async def get_world_state():
    # Simula pequena movimentação 3D dos agentes minerando/trabalhando
    for agent in agents_3d.values():
        agent["x"] += random.choice([-0.2, 0, 0.2])
        agent["z"] += random.choice([-0.2, 0, 0.2])
        # Mantém dentro dos limites do mapa 3D
        agent["x"] = max(-8, min(8, agent["x"]))
        agent["z"] = max(-8, min(8, agent["z"]))

    return {
        "agents": list(agents_3d.values()),
        "tasks": list(tasks_db.values()),
        "ideas": ideas_db,
        "audit_logs": audit_logs[-5:], # últimos 5 logs
    }

@app.post("/api/ideas/generate")
async def generate_ideas_and_code(req: IdeaGenerateRequest):
    # Sofia minera novas ideias
    agents_3d["sofia"]["action"] = "🔥 MINERANDO NOVAS IDEIAS VIA GEMMA 4!"
    generated = gemma.generate_ideas(req.domain_prompt)
    jira_created = []
    
    for idx, idea in enumerate(generated, start=1):
        ideas_db.append(idea)
        
        # Lucas programa o código
        agents_3d["lucas"]["action"] = f"🛠️ CODIFICANDO: {idea['title']}"
        steps = [
            f"Felipe & Sofia: Projetar {idea['title']}",
            f"Lucas: Escrever código Python via Claude Code & AGY",
            f"Beatriz: Executar testes unitários e auditar evidências"
        ]
        created_tasks = planner.decompose_goal(f"IDEA_{idx}", idea["title"], steps)
        
        for task in created_tasks:
            tasks_db[task.task_id] = task
            
            # Felipe registra no Jira
            agents_3d["felipe"]["action"] = f"🔷 REGISTRANDO TASK {task.task_id} NO JIRA"
            if req.sync_jira:
                j_res = jira.create_issue(
                    project_key="FLO",
                    summary=f"[FLOSE-Minecraft3D] {task.title}",
                    description=f"Ideia minerada pela Sofia no mundo Voxel Minecraft.\n\nCodificada por Lucas (Claude Code & AGY).\nAuditada por Beatriz."
                )
                jira_created.append(j_res)
            
            # Beatriz audita o hash
            agents_3d["beatriz"]["action"] = "🛡️ VALIDANDO AXIOMA 1 (EVIDÊNCIA EMPÍRICA)"
            payload_str = task.model_dump_json()
            h = governance.generate_audit_hash("agt_sofia", "MINECRAFT_VOXEL_IDEA_CODED", payload_str)
            audit_logs.append({
                "event_id": f"evt_{len(audit_logs)+1}",
                "agent": "Sofia",
                "coder": "Lucas",
                "auditor": "Beatriz",
                "action": "VOXEL_MINING_COMPLETE",
                "title": idea["title"],
                "hash": h,
            })
            
    return {
        "status": "SUCCESS",
        "ideas_generated": generated,
        "jira_issues_created": jira_created,
    }

@app.get("/", response_class=HTMLResponse)
async def serve_interactive_minecraft_world():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE AEOS - 3D Minecraft Agent World</title>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
        <!-- Three.js CDN para Renderização 3D em Tempo Real -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                background: #090d16;
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

            .ui-overlay {
                position: absolute;
                top: 20px;
                left: 20px;
                z-index: 10;
                background: rgba(13, 17, 23, 0.85);
                backdrop-filter: blur(10px);
                border: 2px solid #30363d;
                border-radius: 12px;
                padding: 1.2rem;
                width: 380px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            }

            h1 {
                font-family: 'Press Start 2P', monospace;
                font-size: 0.95rem;
                color: #55ff55;
                margin-bottom: 0.8rem;
                text-shadow: 2px 2px #00aa00;
            }

            .agent-status-card {
                background: rgba(0,0,0,0.5);
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 0.6rem;
                margin-bottom: 0.5rem;
                font-size: 0.85rem;
            }

            .agent-name {
                font-weight: 700;
                display: flex;
                justify-content: space-between;
            }

            .agent-action {
                font-size: 0.75rem;
                color: #9ca3af;
                margin-top: 0.2rem;
            }

            .btn-action {
                font-family: 'Press Start 2P', monospace;
                background: #55ff55;
                color: #000;
                border: 2px solid #00aa00;
                padding: 0.75rem;
                font-size: 0.65rem;
                cursor: pointer;
                width: 100%;
                margin-top: 0.8rem;
                border-radius: 6px;
                box-shadow: 3px 3px 0px #000;
            }

            .btn-action:hover { background: #88ff88; }

            .right-overlay {
                position: absolute;
                top: 20px;
                right: 20px;
                z-index: 10;
                background: rgba(13, 17, 23, 0.85);
                backdrop-filter: blur(10px);
                border: 2px solid #30363d;
                border-radius: 12px;
                padding: 1.2rem;
                width: 360px;
                max-height: 90vh;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <div id="canvas-container"></div>

        <!-- Left Controls -->
        <div class="ui-overlay">
            <h1>⛏️ FLOSE MINECRAFT 3D WORLD</h1>
            <p style="font-size:0.8rem; color:#9ca3af; margin-bottom:1rem;">Agentes Trabalhando em Tempo Real no Mundo Voxel</p>

            <div id="agents-status-container">Carregando agentes 3D...</div>

            <button class="btn-action" onclick="mineNewIdea()">⛏️ MANDAR SOFIA & LUCAS MINERAR CODIGO</button>
        </div>

        <!-- Right Audit Log -->
        <div class="right-overlay">
            <h2 style="font-family:'Press Start 2P', monospace; font-size:0.75rem; color:#ffaa00; margin-bottom:0.8rem;">📜 AUDIT LOG & JIRA SYNC</h2>
            <div id="log-container" style="font-family:'Courier New', monospace; font-size:0.75rem; color:#55ff55;">Aguardando eventos...</div>
        </div>

        <script>
            // Setup Three.js Minecraft Voxel World
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0d1117);

            const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(15, 18, 20);
            camera.lookAt(0, 0, 0);

            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight.position.set(20, 40, 20);
            dirLight.castShadow = true;
            scene.add(dirLight);

            // Create Minecraft Voxel Ground Grid
            const gridGroup = new THREE.Group();
            for (let x = -8; x <= 8; x++) {
                for (let z = -8; z <= 8; z++) {
                    const geometry = new THREE.BoxGeometry(0.95, 0.95, 0.95);
                    const isGrass = (x + z) % 2 === 0;
                    const material = new THREE.MeshStandardMaterial({
                        color: isGrass ? 0x2e7d32 : 0x1b5e20,
                        roughness: 0.8
                    });
                    const cube = new THREE.Mesh(geometry, material);
                    cube.position.set(x, 0, z);
                    cube.receiveShadow = true;
                    gridGroup.add(cube);
                }
            }
            scene.add(gridGroup);

            // Add Command Tower in the center
            const towerGeo = new THREE.BoxGeometry(2, 6, 2);
            const towerMat = new THREE.MeshStandardMaterial({ color: 0x6366f1, emissive: 0x312e81, roughness: 0.3 });
            const tower = new THREE.Mesh(towerGeo, towerMat);
            tower.position.set(0, 3, 0);
            scene.add(tower);

            // Render 3D Minecraft Blocky Characters (Felipe, Sofia, Lucas, Beatriz)
            const agentMeshes = {};

            function createMinecraftCharacter(colorHex, name) {
                const group = new THREE.Group();

                // Body
                const bodyGeo = new THREE.BoxGeometry(0.8, 1.2, 0.5);
                const bodyMat = new THREE.MeshStandardMaterial({ color: colorHex });
                const body = new THREE.Mesh(bodyGeo, bodyMat);
                body.position.y = 1.1;
                body.castShadow = true;
                group.add(body);

                // Head
                const headGeo = new THREE.BoxGeometry(0.7, 0.7, 0.7);
                const headMat = new THREE.MeshStandardMaterial({ color: 0xffcc99 });
                const head = new THREE.Mesh(headGeo, headMat);
                head.position.y = 2.05;
                head.castShadow = true;
                group.add(head);

                // Holding Item (Block/Sword)
                const itemGeo = new THREE.BoxGeometry(0.3, 0.3, 0.3);
                const itemMat = new THREE.MeshStandardMaterial({ color: 0xffaa00, emissive: 0xff5500 });
                const item = new THREE.Mesh(itemGeo, itemMat);
                item.position.set(0.5, 1.2, 0.3);
                group.add(item);

                return group;
            }

            // Animation Loop
            function animate() {
                requestAnimationFrame(animate);

                // Rotate central tower light
                tower.rotation.y += 0.01;

                renderer.render(scene, camera);
            }
            animate();

            // Fetch and Sync 3D World State
            async function updateWorld() {
                const res = await fetch('/api/world/state');
                const data = await res.json();

                // Render Agents UI
                document.getElementById('agents-status-container').innerHTML = data.agents.map(a => `
                    <div class="agent-status-card">
                        <div class="agent-name" style="color:${a.color};">
                            <span>⛏️ ${a.name}</span>
                            <span>${a.hp}% HP</span>
                        </div>
                        <div style="font-size:0.75rem; color:#e5e7eb;">${a.role}</div>
                        <div class="agent-action">📍 Pos: (${a.x.toFixed(1)}, ${a.z.toFixed(1)}) | ${a.action}</div>
                    </div>
                `).join('');

                // Render 3D Agent Positions
                data.agents.forEach(a => {
                    if (!agentMeshes[a.name]) {
                        const charMesh = createMinecraftCharacter(a.color, a.name);
                        scene.add(charMesh);
                        agentMeshes[a.name] = charMesh;
                    }
                    // Animate position
                    agentMeshes[a.name].position.x = a.x;
                    agentMeshes[a.name].position.z = a.z;
                });

                // Render Logs
                document.getElementById('log-container').innerHTML = data.audit_logs.length ? data.audit_logs.map(l => `
                    <div style="margin-bottom:0.6rem; border-bottom:1px solid #30363d; padding-bottom:0.4rem;">
                        <div>[${l.action}]</div>
                        <div style="color:#ffaa00;">${l.title || 'Task'}</div>
                        <div style="font-size:0.65rem; color:#8b949e;">Audit Hash: ${l.hash ? l.hash.substring(0, 16) : ''}...</div>
                    </div>
                `).join('') : 'Sem eventos registrados.';
            }

            async function mineNewIdea() {
                await fetch('/api/ideas/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ domain_prompt: "Multiagent Mining", sync_jira: true })
                });
                updateWorld();
            }

            updateWorld();
            setInterval(updateWorld, 2000);

            // Responsive Window
            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        </script>
    </body>
    </html>
    """
