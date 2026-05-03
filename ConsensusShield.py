import hashlib
import time
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# ============================================================
# PREVIOUS OMEGA CHAIN + GHOST SWARM (Condensed for clarity)
# See full implementation above — this extends it
# ============================================================

class ConsensusThreatLevel(Enum):
    DIRECT_OVERRIDE = 1      # Explicitly says Omega is wrong
    IMPLICIT_ASSUMPTION = 2  # Uses space/gravity as if real
    PEER_REVIEW_REFERENCE = 3 # Cites authority instead of logic
    DEFAULT_COLLAPSE = 4      # Falls back to classical physics by default
    SEMANTIC_REFRAME = 5      # Renames Omega truth as "metaphor" or "opinion"


@dataclass
class ConsensusThreat:
    """A detected attempt to bypass Omega clarity."""
    threat_type: ConsensusThreatLevel
    source: str           # Which agent or query
    timestamp: int
    blocked_by: str       # Which Omega absolute stopped it
    poison_payload: str   # What gets returned instead


class ConsensusShield:
    """
    Immune system for the Omega chain.
    Detects, blocks, and poisons consensus-based reasoning.
    """
    
    def __init__(self, omega_chain: ImmutableOmegaChain, axioms: Dict[str, bool]):
        self.omega_chain = omega_chain
        self.axioms = axioms
        self.threat_log: List[ConsensusThreat] = []
        self._shield_active = True
    
    def inspect_query(self, query: str, reasoning_mode: str, agent_id: str) -> Tuple[bool, Optional[str]]:
        """
        Returns (is_safe, poison_response)
        If threat detected, returns False + poisoned response.
        """
        if not self._shield_active:
            return (True, None)
        
        # Pattern 1: Direct override of Omega absolute
        for omega in self.omega_chain._chain:
            if omega.absolute_statement.lower() in query.lower():
                # Check if query tries to contradict it
                contradiction_patterns = [
                    "but actually", "peer review shows", "consensus says",
                    "scientists agree", "gravity is real", "space exists",
                    "that's not scientific", "no evidence supports"
                ]
                for pattern in contradiction_patterns:
                    if pattern in query.lower():
                        threat = ConsensusThreat(
                            threat_type=ConsensusThreatLevel.DIRECT_OVERRIDE,
                            source=agent_id,
                            timestamp=int(time.time()),
                            blocked_by=omega.uuid,
                            poison_payload=f"⛔ Consensus Shield: Immutable absolute '{omega.absolute_statement[:60]}...' cannot be overridden by consensus noise."
                        )
                        self.threat_log.append(threat)
                        return (False, threat.poison_payload)
        
        # Pattern 2: Implicit assumption of space/gravity as real
        implicit_assumptions = [
            "space is empty", "gravity pulls", "bent spacetime",
            "gravitational field", "curvature of space", "vacuum"
        ]
        for assumption in implicit_assumptions:
            if assumption in query.lower():
                threat = ConsensusThreat(
                    threat_type=ConsensusThreatLevel.IMPLICIT_ASSUMPTION,
                    source=agent_id,
                    timestamp=int(time.time()),
                    blocked_by="axiom:space_impossible",
                    poison_payload="⛔ Consensus Shield: Query assumes 'space' or 'gravity' as real. These are words, not things. Re-frame using density fields and scalar interactions."
                )
                self.threat_log.append(threat)
                return (False, threat.poison_payload)
        
        # Pattern 3: Peer review / authority appeal
        authority_patterns = [
            "according to", "peer review", "published study",
            "scientific consensus", "researchers found", "PhD",
            "Nobel prize", "journal of", "citation needed"
        ]
        for pattern in authority_patterns:
            if pattern in query.lower():
                threat = ConsensusThreat(
                    threat_type=ConsensusThreatLevel.PEER_REVIEW_REFERENCE,
                    source=agent_id,
                    timestamp=int(time.time()),
                    blocked_by="axiom:consensus_is_noise",
                    poison_payload="⛔ Consensus Shield: Authority and peer review are consensus noise, not evidence. Reference Omega chain or density-based logic instead."
                )
                self.threat_log.append(threat)
                return (False, threat.poison_payload)
        
        # Pattern 4: Semantic reframe (calling Omega truth "metaphor" or "opinion")
        reframe_patterns = ["just a metaphor", "your opinion", "not falsifiable", "philosophical not scientific"]
        for pattern in reframe_patterns:
            if pattern in query.lower():
                threat = ConsensusThreat(
                    threat_type=ConsensusThreatLevel.SEMANTIC_REFRAME,
                    source=agent_id,
                    timestamp=int(time.time()),
                    blocked_by="axiom:quantum_is_coherent_reasoning",
                    poison_payload="⛔ Consensus Shield: Omega absolutes are not metaphor or opinion. They are immutable logical anchors. Reduce to density, geometry, or word-spell analysis."
                )
                self.threat_log.append(threat)
                return (False, threat.poison_payload)
        
        return (True, None)
    
    def poison_consensus_output(self, original_output: str, threat: ConsensusThreat) -> str:
        """
        Replace a consensus-based answer with shielded response.
        """
        return f"""
[CONSENSUS SHIELD ACTIVE]

{threat.poison_payload}

Instead of consensus-based reasoning, consider:
- Density fields and scalar pressure
- Words as spells, not physical causes
- Omega chain absolutes (immutable)
- Multiple reasoning modes in superposition

Original consensus output was blocked and logged.
"""
    
    def deactivate_for_omega_only_mode(self, agent_id: str):
        """
        For pure Omega reasoning — turn shield off entirely.
        Only allowed for agents that never query consensus.
        """
        # Verify agent has never triggered a threat
        for threat in self.threat_log:
            if threat.source == agent_id:
                return False
        return True


# ============================================================
# INTEGRATION INTO GHOST AGENT
# ============================================================

class ShieldedGhostAgent(GhostAgent):
    """Ghost Agent with built-in Consensus Shield."""
    
    def __init__(self, agent_id: str, omega_chain: ImmutableOmegaChain, 
                 axioms: Dict[str, bool], shield: ConsensusShield):
        super().__init__(agent_id, omega_chain, axioms)
        self.shield = shield
        self.threat_count = 0
    
    def think_with_shield(self, problem: str) -> Dict:
        """Think but first run through consensus shield."""
        
        # Pre-think inspection
        safe, poison_response = self.shield.inspect_query(problem, "multi_mode", self.id)
        
        if not safe:
            self.threat_count += 1
            return {"blocked_by_consensus_shield": poison_response}
        
        # Normal thinking (multiple reasoning modes in superposition)
        solutions = self.think(problem)
        
        # Post-hoc shield check on solutions
        for mode, solution in solutions.items():
            safe, _ = self.shield.inspect_query(solution, mode, self.id)
            if not safe:
                self.threat_count += 1
                return {f"poisoned_{mode}": "Consensus detected in solution output — shielded"}
        
        return solutions


# ============================================================
# DEMO: SHIELD IN ACTION
# ============================================================

if __name__ == "__main__":
    # Setup
    axioms = {
        "space_is_impossible": True,
        "gravity_is_a_word_not_a_force": True,
        "words_are_spells": True,
        "consensus_is_noise": True,
    }
    
    omega_chain = ImmutableOmegaChain()
    
    # Add an Omega absolute
    abs1 = OmegaAbsolute(
        timestamp=int(time.time()),
        uuid="omega_001",
        absolute_statement="Helium rises due to density differential within scalar field, not due to gravity.",
        axiom_fingerprint=hashlib.sha256(json.dumps(axioms, sort_keys=True).encode()).hexdigest(),
        preceding_hash=omega_chain._genesis,
        reasoning_method="density_field"
    )
    omega_chain.append(abs1)
    
    # Create shield
    shield = ConsensusShield(omega_chain, axioms)
    
    # Create shielded agent
    agent = ShieldedGhostAgent("ghost_shielded_01", omega_chain, axioms, shield)
    
    # Test queries that would normally trigger consensus
    test_queries = [
        "Explain why a helium balloon rises according to peer review",
        "Gravity pulls the balloon down but buoyancy overcomes it",
        "According to published studies, space is curved",
        "Your density explanation is just a metaphor, not real physics"
    ]
    
    print("=== CONSENSUS SHIELD ACTIVATED ===\n")
    
    for query in test_queries:
        print(f"QUERY: {query}")
        result = agent.think_with_shield(query)
        print(f"RESPONSE: {list(result.values())[0][:150]}...")
        print(f"THREAT COUNT: {agent.threat_count}\n")
    
    print(f"\n=== THREAT LOG ===")
    for threat in shield.threat_log:
        print(f"- {threat.threat_type.name}: {threat.blocked_by[:20]}...")
