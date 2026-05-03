pip install pyautogen langgraph langchain
# ============================================================
# PERSISTENCE LAYER — Omega Chain saves across sessions
# ============================================================

from replit import db  # Replit's built-in database

def save_omega_chain(swarm):
    """Store Omega chain and swarm state"""
    db["omega_chain"] = [{
        "uuid": a.uuid,
        "statement": a.absolute_statement,
        "timestamp": a.timestamp
    } for a in swarm.omega_chain._chain]
    db["num_agents"] = len(swarm.agents)
    db["last_saved"] = time.time()

def load_omega_chain(swarm):
    """Restore from database on startup"""
    if "omega_chain" in db:
        # Reconstruction logic here
        print(f"Loaded {len(db['omega_chain'])} Omega points from memory")
