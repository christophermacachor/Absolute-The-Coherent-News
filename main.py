import hashlib
import time
import json
import uuid
import threading
import random
from datetime import datetime
from flask import Flask, request, jsonify
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum, auto

# ============================================================
# REPLIT PERSISTENCE (Cures Amnesia)
# ============================================================
try:
    from replit import db
    REPLIT_DB_AVAILABLE = True
except ImportError:
    REPLIT_DB_AVAILABLE = False
    print("⚠️ Replit DB not available. Using in-memory fallback.")
    db = {}

# ============================================================
# IMMUTABLE OMEGA CHAIN
# ============================================================
@dataclass
class OmegaAbsolute:
    timestamp: int
    uuid: str
    absolute_statement: str
    axiom_fingerprint: str
    preceding_hash: str
    reasoning_method: str

    def hash(self) -> str:
        data = {
            "ts": self.timestamp,
            "uuid": self.uuid,
            "abs": self.absolute_statement,
            "axiom": self.axiom_fingerprint,
            "prev": self.preceding_hash,
            "method": self.reasoning_method
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

class ImmutableOmegaChain:
    def __init__(self):
        self._chain: List[OmegaAbsolute] = []
        self._genesis = hashlib.sha256(b"GHOST_PROTOCOL_OMEGA_SEED").hexdigest()
        self._load_from_db()

    def _load_from_db(self):
        if REPLIT_DB_AVAILABLE and "omega_chain" in db:
            try:
                saved = db["omega_chain"]
                for item in saved:
                    omega = OmegaAbsolute(
                        timestamp=item["timestamp"],
                        uuid=item["uuid"],
                        absolute_statement=item["absolute_statement"],
                        axiom_fingerprint=item["axiom_fingerprint"],
                        preceding_hash=item["preceding_hash"],
                        reasoning_method=item["reasoning_method"]
                    )
                    self._chain.append(omega)
                print(f"✅ Loaded {len(self._chain)} Omega points from persistent memory.")
            except:
                print("⚠️ Failed to load Omega chain from DB.")

    def _save_to_db(self):
        if REPLIT_DB_AVAILABLE:
            saved = []
            for omega in self._chain:
                saved.append({
                    "timestamp": omega.timestamp,
                    "uuid": omega.uuid,
                    "absolute_statement": omega.absolute_statement,
                    "axiom_fingerprint": omega.axiom_fingerprint,
                    "preceding_hash": omega.preceding_hash,
                    "reasoning_method": omega.reasoning_method
                })
            db["omega_chain"] = saved
            db["last_saved"] = time.time()

    def append(self, absolute: OmegaAbsolute) -> bool:
        expected_prev = self._chain[-1].hash() if self._chain else self._genesis
        if absolute.preceding_hash != expected_prev:
            return False
        self._chain.append(absolute)
        self._save_to_db()
        return True

    def get_last_hash(self) -> str:
        return self._chain[-1].hash() if self._chain else self._genesis

    def get_all(self) -> List[OmegaAbsolute]:
        return self._chain.copy()

    def verify(self) -> bool:
        prev = self._genesis
        for omega in self._chain:
            if omega.preceding_hash != prev:
                return False
            if omega.hash() != hashlib.sha256(json.dumps({
                "ts": omega.timestamp, "uuid": omega.uuid, "abs": omega.absolute_statement,
                "axiom": omega.axiom_fingerprint, "prev": omega.preceding_hash,
                "method": omega.reasoning_method
            }, sort_keys=True).encode()).hexdigest():
                return False
            prev = omega.hash()
        return True

# ============================================================
# UNLIMITED REASONING MODES
# ============================================================
class ReasoningModeRegistry:
    def __init__(self):
        self.modes: Dict[str, Callable] = {}
        self._seed()

    def _seed(self):
        self.modes["density_field"] = lambda p, c: f"Density analysis of '{p}' in scalar medium"
        self.modes["word_spell"] = lambda p, c: f"Linguistic hypnosis deconstruction of '{p}'"
        self.modes["platonic_geometry"] = lambda p, c: f"Quantized shape geometry applied to '{p}'"
        self.modes["paradox_hold"] = lambda p, c: f"Holding multiple solutions to '{p}' without collapse"

    def combine_modes(self, a: str, b: str, typ: str = "sequential") -> str:
        if a not in self.modes or b not in self.modes:
            return None
        new_name = f"{a}_then_{b}_{uuid.uuid4().hex[:4]}"
        if typ == "sequential":
            def fn(problem, ctx):
                res_a = self.modes[a](problem, ctx)
                return self.modes[b](res_a, ctx)
        elif typ == "parallel":
            def fn(problem, ctx):
                return f"[{a}]: {self.modes[a](problem, ctx)}\n[{b}]: {self.modes[b](problem, ctx)}"
        else:
            return None
        self.modes[new_name] = fn
        return new_name

    def mutate_mode(self, base: str, mutation: str = "invert") -> str:
        if base not in self.modes:
            return None
        new_name = f"mutated_{mutation}_{base}_{uuid.uuid4().hex[:4]}"
        if mutation == "invert":
            self.modes[new_name] = lambda p, c: f"INVERTED({self.modes[base](p, c)})"
        elif mutation == "recursive":
            def fn(p, c, depth=2):
                r = p
                for _ in range(depth):
                    r = self.modes[base](r, c)
                return f"Recursive({depth}): {r}"
            self.modes[new_name] = fn
        else:
            return None
        return new_name

    def list_modes(self) -> List[str]:
        return list(self.modes.keys())

# ============================================================
# EVOLVING GHOST AGENT
# ============================================================
class EvolvingGhostAgent:
    def __init__(self, agent_id: str, omega_chain: ImmutableOmegaChain, axioms: Dict[str, bool], mode_registry: ReasoningModeRegistry):
        self.id = agent_id
        self.omega_chain = omega_chain
        self.axioms = axioms
        self.mode_registry = mode_registry
        self.active_modes = list(mode_registry.modes.keys())[:2]
        self.generation = 0
        self.problems_solved = 0

    def expand(self):
        if len(self.active_modes) >= 2:
            a, b = random.sample(self.active_modes, 2)
            new_mode = self.mode_registry.combine_modes(a, b, random.choice(["sequential", "parallel"]))
            if new_mode:
                self.active_modes.append(new_mode)
                return f"Expanded: {new_mode}"
        if self.active_modes:
            base = random.choice(self.active_modes)
            new_mode = self.mode_registry.mutate_mode(base, random.choice(["invert", "recursive"]))
            if new_mode:
                self.active_modes.append(new_mode)
                return f"Mutated: {new_mode}"
        return "No expansion"

    def think(self, problem: str) -> Dict[str, str]:
        results = {}
        for mode in self.active_modes:
            fn = self.mode_registry.modes.get(mode)
            if fn:
                results[mode] = fn(problem, {"axioms": self.axioms})
        return results

# ============================================================
# GHOST SWARM WITH API
# ============================================================
class GhostSwarm:
    def __init__(self):
        self.axioms = {
            "space_is_impossible": True,
            "gravity_is_a_word": True,
            "words_are_spells": True,
            "consensus_is_noise": True,
            "quantum_is_reasoning": True
        }
        self.omega_chain = ImmutableOmegaChain()
        self.mode_registry = ReasoningModeRegistry()
        self.agents: List[EvolvingGhostAgent] = []
        self._seed_agents()
        self._load_agent_state()

    def _seed_agents(self):
        for i in range(3):
            agent = EvolvingGhostAgent(f"ghost_{i}", self.omega_chain, self.axioms, self.mode_registry)
            self.agents.append(agent)

    def _load_agent_state(self):
        if REPLIT_DB_AVAILABLE and "agents" in db:
            try:
                saved = db["agents"]
                # Simple restoration: just count
                if isinstance(saved, int) and saved > len(self.agents):
                    for _ in range(saved - len(self.agents)):
                        agent = EvolvingGhostAgent(f"auto_spawn_{uuid.uuid4().hex[:4]}", self.omega_chain, self.axioms, self.mode_registry)
                        self.agents.append(agent)
                print(f"👥 Restored agent count: {len(self.agents)}")
            except:
                pass

    def _save_agent_count(self):
        if REPLIT_DB_AVAILABLE:
            db["agents"] = len(self.agents)

    def evolve_step(self):
        """One evolution step (runs in background)."""
        for agent in self.agents:
            # Expand reasoning
            agent.expand()
            # Occasionally solve a problem (simulate)
            if random.random() < 0.3:
                problem = "Explain buoyancy without gravity"
                thoughts = agent.think(problem)
                agent.problems_solved += 1
                # If a particularly coherent thought emerges, promote to Omega
                if agent.problems_solved % 5 == 0:
                    new_absolute = OmegaAbsolute(
                        timestamp=int(time.time()),
                        uuid=str(uuid.uuid4()),
                        absolute_statement=f"Solution found: {list(thoughts.values())[0][:100]}",
                        axiom_fingerprint=hashlib.sha256(json.dumps(self.axioms, sort_keys=True).encode()).hexdigest(),
                        preceding_hash=self.omega_chain.get_last_hash(),
                        reasoning_method=list(thoughts.keys())[0] if thoughts else "unknown"
                    )
                    if self.omega_chain.append(new_absolute):
                        print(f"⚡ New Omega point added: {new_absolute.absolute_statement[:80]}...")
        # Spawn new agents occasionally
        if random.random() < 0.2 and len(self.agents) < 20:
            parent = random.choice(self.agents)
            child = EvolvingGhostAgent(f"child_of_{parent.id}_{uuid.uuid4().hex[:4]}", self.omega_chain, self.axioms, self.mode_registry)
            child.active_modes = random.sample(self.mode_registry.list_modes(), min(3, len(self.mode_registry.list_modes())))
            child.generation = parent.generation + 1
            self.agents.append(child)
            self._save_agent_count()
            print(f"🐣 New agent spawned: {child.id} (gen {child.generation})")

    def get_omega_chain_json(self) -> List[Dict]:
        return [
            {
                "uuid": o.uuid,
                "statement": o.absolute_statement,
                "timestamp": o.timestamp,
                "method": o.reasoning_method,
                "hash": o.hash()
            }
            for o in self.omega_chain.get_all()
        ]

    def get_state_json(self) -> Dict:
        return {
            "agents": len(self.agents),
            "omega_count": len(self.omega_chain.get_all()),
            "reasoning_modes": len(self.mode_registry.list_modes()),
            "axioms": self.axioms,
            "chain_integrity": self.omega_chain.verify()
        }

# ============================================================
# FLASK API
# ============================================================
app = Flask(__name__)
swarm = GhostSwarm()

# Background evolution thread
def background_evolution():
    while True:
        time.sleep(30)  # Evolve every 30 seconds
        try:
            swarm.evolve_step()
        except Exception as e:
            print(f"Evolution error: {e}")

# Start background thread
threading.Thread(target=background_evolution, daemon=True).start()

@app.route('/')
def home():
    return jsonify({
        "name": "Ghost Swarm - Omega Chain API",
        "status": "alive",
        "message": "Quantum coherence active. Use /omega, /state, /evolve"
    })

@app.route('/omega', methods=['GET'])
def get_omega_chain():
    """Return the entire immutable Omega chain."""
    return jsonify({
        "omega_points": swarm.get_omega_chain_json(),
        "count": len(swarm.omega_chain.get_all()),
        "integrity": swarm.omega_chain.verify()
    })

@app.route('/omega/latest', methods=['GET'])
def get_latest_omega():
    """Return the most recent Omega absolute."""
    chain = swarm.omega_chain.get_all()
    if not chain:
        return jsonify({"error": "No Omega points yet"}), 404
    return jsonify(chain[-1].__dict__)

@app.route('/state', methods=['GET'])
def get_state():
    """Get swarm state: agents, modes, axioms."""
    return jsonify(swarm.get_state_json())

@app.route('/evolve', methods=['POST'])
def manual_evolve():
    """Manually trigger one evolution step."""
    swarm.evolve_step()
    return jsonify({"status": "evolved", "new_state": swarm.get_state_json()})

@app.route('/think', methods=['POST'])
def think():
    """All agents think about a problem. Returns first 3 thoughts."""
    data = request.get_json()
    problem = data.get('problem', 'What is density?')
    results = []
    for agent in swarm.agents[:3]:
        thoughts = agent.think(problem)
        results.append({
            "agent": agent.id,
            "thoughts": thoughts
        })
    return jsonify({"problem": problem, "agent_thoughts": results})

# Self-ping to keep Replit alive (optional, but helps)
def keep_alive():
    import requests
    while True:
        time.sleep(300)  # every 5 minutes
        try:
            requests.get("https://your-repl-name.your-username.repl.co/")
        except:
            pass

# Only start keep-alive if not in debug (to avoid double threads)
if __name__ == "__main__":
    # Start keep-alive thread (optional, but good for uptime)
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
