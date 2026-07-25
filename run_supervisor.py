import time
import urllib.request
import urllib.error
import sqlite3
import subprocess
import os
import sys

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(REPO_PATH, "data", "persistence", "flose_state.db")
SERVER_URL = "http://127.0.0.1:8085/api/boss/state"
CHECK_INTERVAL = 3  # seconds
MAX_FAILURES = 3

def print_banner():
    print("\n" + "="*50)
    print("🛡️  FLOSE AEOS - SUPERVISOR SENTINEL 🛡️")
    print("="*50 + "\n")

def check_server_health() -> bool:
    try:
        req = urllib.request.Request(SERVER_URL, method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except urllib.error.URLError:
        return False
    except Exception:
        return False

def check_git_status() -> bool:
    """Retorna True se o repositório estiver limpo (sem arquivos modificados)."""
    try:
        res = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_PATH, capture_output=True, text=True)
        return len(res.stdout.strip()) == 0
    except Exception:
        return True

def auto_heal_repository():
    """Restaura os arquivos para o último commit seguro."""
    print("🚨 [CRÍTICO] Servidor caiu! Iniciando protocolo de Auto-Recovery (Rollback)...")
    try:
        # Desfaz qualquer mudança não commitada que possa ter quebrado a sintaxe
        subprocess.run(["git", "restore", "."], cwd=REPO_PATH, check=True)
        print("✅ [RECOVERY] Git restore executado. Código mutante defeituoso foi revertido.")
        # O Uvicorn com --reload deve pegar a restauração e subir o server novamente!
    except Exception as e:
        print(f"❌ [ERRO] Falha ao executar o Auto-Recovery: {e}")

def get_latest_events(limit=3):
    if not os.path.exists(DB_PATH):
        return []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, action, details FROM domain_events ORDER BY id DESC LIMIT ?", (limit,))
        events = cursor.fetchall()
        conn.close()
        return events
    except sqlite3.Error:
        return []

def main():
    print_banner()
    consecutive_failures = 0
    
    while True:
        is_alive = check_server_health()
        is_git_clean = check_git_status()
        
        timestamp = time.strftime("%H:%M:%S")
        
        if is_alive:
            consecutive_failures = 0
            status_symbol = "🟢 ONLINE"
        else:
            consecutive_failures += 1
            status_symbol = f"🔴 OFFLINE ({consecutive_failures}/{MAX_FAILURES})"
            
        git_symbol = "✨ CLEAN" if is_git_clean else "⚠️ MUTATED"
        
        print(f"[{timestamp}] API: {status_symbol} | Workspace: {git_symbol}", end="")
        sys.stdout.flush()
        
        # Monitoramento de DB
        events = get_latest_events(1)
        if events:
            evt_time, action, details = events[0]
            print(f" | Último Evento: {action} ({evt_time[11:19]})")
        else:
            print()
            
        if consecutive_failures >= MAX_FAILURES:
            auto_heal_repository()
            print("⏳ Aguardando Uvicorn reiniciar (10s)...")
            time.sleep(10)
            consecutive_failures = 0
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Supervisor encerrado pelo usuário.")
