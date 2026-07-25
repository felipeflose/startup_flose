import os
import json
import asyncio
from typing import Dict, Any, Tuple, List

REPO_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(REPO_PATH, "data")
PERSISTENCE_FILE = os.path.join(DATA_DIR, "state_persistence.json")

_save_lock = asyncio.Lock()

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_persisted_state() -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, Any]]]:
    """
    Carrega o estado persistido do jogo (Game State, Pixel Agents, Audit Logs) do disco se existir.
    Retorna (game_state, pixel_agents, audit_logs) ou (None, None, None) se não existir.
    """
    ensure_data_dir()
    if not os.path.exists(PERSISTENCE_FILE):
        return None, None, None

    try:
        with open(PERSISTENCE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        game_state = data.get("game_state")
        pixel_agents = data.get("pixel_agents")
        audit_logs = data.get("audit_logs", [])

        if game_state and pixel_agents:
            print(f"[Persistence] State loaded successfully from {PERSISTENCE_FILE}")
            return game_state, pixel_agents, audit_logs
    except Exception as e:
        print(f"[Persistence Load Error] {e}")

    return None, None, None


async def save_state_to_disk(game_state: Dict[str, Any], pixel_agents: Dict[str, Any], audit_logs: List[Dict[str, Any]]):
    """
    Salva assincronamente o estado atual do jogo no disco em data/state_persistence.json.
    """
    async with _save_lock:
        ensure_data_dir()
        try:
            payload = {
                "game_state": game_state,
                "pixel_agents": pixel_agents,
                "audit_logs": audit_logs[-50:]  # Mantém os últimos 50 logs de auditoria
            }
            
            # Escreve em um arquivo temporário primeiro e depois substitui (escrita atômica)
            temp_file = PERSISTENCE_FILE + ".tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)

            os.replace(temp_file, PERSISTENCE_FILE)
        except Exception as e:
            print(f"[Persistence Save Error] {e}")
