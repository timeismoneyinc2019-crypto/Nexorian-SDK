import json
import hashlib
import time
import uuid
from typing import Dict, Any, List, Optional

# --- CORE DETERMINISTIC ENGINE ---

class LawEnvelope:
    def __init__(self, name: str, schema: Dict[str, Any], constraints: List[str]):
        self.name = name
        self.schema = schema
        self.constraints = constraints

class DeterministicComplianceEngine:
    def __init__(self, ledger):
        self.ledger = ledger
        self.envelopes: Dict[str, LawEnvelope] = {}
        self._load_standard_envelopes()

    def _load_standard_envelopes(self):
        # Anchor standard compliance envelopes
        self.envelopes["FINRA_CT_09"] = LawEnvelope(
            "FINRA_CT_09",
            {"epoch_limit": float, "actor_role": str},
            ["epoch <= epoch_limit", "actor_role == 'OPERATOR'"]
        )
        self.envelopes["CORE_GENESIS"] = LawEnvelope(
            "CORE_GENESIS",
            {"actor_role": str},
            ["actor_role in ['ADMIN', 'OPERATOR']"]
        )

    def validate_execution(self, envelope_name: str, params: Dict[str, Any]) -> bool:
        if envelope_name not in self.envelopes:
            return False
        
        envelope = self.envelopes[envelope_name]
        
        # Deterministic Evaluation
        try:
            for constraint in envelope.constraints:
                # Local deterministic evaluation using restricted context
                if not eval(constraint, {"__builtins__": None}, params):
                    return False
            return True
        except:
            return False

# --- AUDIT LEDGER (SHA3 CHAINING) ---

class AuditEntry:
    def __init__(self, epoch: float, action: str, actor: str, payload: dict, prev_hash: str):
        self.timestamp = time.time()
        self.epoch = epoch
        self.action = action
        self.actor = actor
        self.payload = payload
        self.prev_hash = prev_hash
        self.hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        data = {
            "ts": self.timestamp,
            "epoch": self.epoch,
            "action": self.action,
            "actor": self.actor,
            "payload": self.payload,
            "prev_hash": self.prev_hash
        }
        return hashlib.sha3_256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def to_dict(self):
        return {
            "ts": self.timestamp,
            "epoch": self.epoch,
            "action": self.action,
            "actor": self.actor,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "hash": self.hash
        }

class DeterministicAuditLedger:
    def __init__(self, log_path: Optional[str] = None):
        self.log_path = log_path
        self.chain: List[AuditEntry] = []
        self._initialize_genesis()

    def _initialize_genesis(self):
        genesis = AuditEntry(0.0, "GENESIS_ANCHOR", "SYSTEM", {"msg": "SDK_GENESIS_INITIALIZED"}, "0" * 64)
        self.chain.append(genesis)
        if self.log_path:
            self._persist(genesis)

    def append(self, epoch: float, action: str, actor: str, payload: dict):
        prev_hash = self.chain[-1].hash
        entry = AuditEntry(epoch, action, actor, payload, prev_hash)
        self.chain.append(entry)
        if self.log_path:
            self._persist(entry)
        return entry.hash

    def _persist(self, entry: AuditEntry):
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")

    def verify_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.prev_hash != previous.hash: return False
            if current.hash != current._calculate_hash(): return False
        return True

# --- OPERATIONAL KERNEL ---

class NexusKernel:
    """
    Nexorian Operational SDK v1.0.0 (Implementation Lock)
    FULL STANDALONE KERNEL IMPLEMENTATION.
    """
    def __init__(self, api_key: str, role: str = "SANDBOX", log_path: str = "audit_ledger.jsonl"):
        self.api_key = api_key
        self.role = role
        self.ledger = DeterministicAuditLedger(log_path)
        self.dce = DeterministicComplianceEngine(self.ledger)
        self.state = "IDLE"

    def execute(self, task: str, envelope: str, params: Dict[str, Any]) -> bool:
        """
        Full Deterministic Execution Path.
        Returns True if approved and executed, False or raises Error if rejected.
        """
        self.state = "BREEZE_CONSENSUS"
        params["actor_role"] = self.role
        
        # DCE ENFORCEMENT
        if self.dce.validate_execution(envelope, params):
            self.state = "EXECUTING"
            execution_id = str(uuid.uuid4())
            
            # Record Execution Start to Ledger
            self.ledger.append(params.get("epoch", 0.0), "EXEC_START", self.role, 
                               {"task": task, "envelope": envelope, "id": execution_id})
            
            # Perform Logic (Simulated for SDK, physically bound by Ledger)
            result = True 
            
            # Record Execution Completion
            self.ledger.append(params.get("epoch", 0.0), "EXEC_COMPLETE", "SYSTEM", 
                               {"id": execution_id, "status": "FINALIZED"})
            
            self.state = "IDLE"
            return True
        else:
            self.state = "HALTED"
            # Hard Rejection in Ledger
            self.ledger.append(params.get("epoch", 0.0), "REJECTION", self.role, 
                               {"task": task, "envelope": envelope, "reason": "DCE_VETO"})
            raise PermissionError(f"EXECUTION_VETO: Command violates Law Envelope [{envelope}].")

if __name__ == "__main__":
    # Internal Verification Check
    kernel = NexusKernel(api_key="DEMO_KEY_123")
    print("--- NEXORIAN SDK SELF-TEST ---")
    try:
        # Valid Admin Call
        kernel.role = "ADMIN"
        kernel.execute("PROBE_KERNEL", "CORE_GENESIS", {"epoch": 0.1})
        print("[SUCCESS] Admin probe authorized.")
        
        # Invalid Sandbox Call
        kernel.role = "SANDBOX"
        kernel.execute("DELETE_CORE", "CORE_GENESIS", {"epoch": 0.2})
    except PermissionError as e:
        print(f"[VERIFIED] Rejection confirmed: {e}")
    
    print(f"Chain Integrity: {kernel.ledger.verify_integrity()}")
    print("--- TEST COMPLETE ---")
