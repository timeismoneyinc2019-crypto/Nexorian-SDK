import json
import hashlib
from typing import Dict, Any, List, Optional

class LawEnvelope:
    def __init__(self, name: str, constraints: List[str]):
        self.name = name
        self.constraints = constraints

class NexusKernel:
    """
    Nexorian Python SDK v1.0.0 (Implementation Lock)
    Includes Local Admissibility Gate and Command Chaining.
    """
    def __init__(self, api_key: str, role: str = "SANDBOX", domain: str = "api.nexorian.org"):
        self.api_key = api_key
        self.role = role
        self.domain = domain
        self.last_hash: str = hashlib.sha256(api_key.encode()).hexdigest() # Genesis Anchor
        
        # Local Compliance Definitions (Must sync with Core)
        self.envelopes: Dict[str, LawEnvelope] = {
            "FINRA_CT_09": LawEnvelope("FINRA_CT_09", ["epoch <= epoch_limit", "actor_role == 'OPERATOR'"]),
            "CORE_GENESIS": LawEnvelope("CORE_GENESIS", ["actor_role in ['ADMIN', 'OPERATOR']"])
        }

    def _validate_local(self, envelope_name: str, params: Dict[str, Any]) -> bool:
        """Admissibility Gate: Local Enforcement before Network Egress"""
        if envelope_name not in self.envelopes:
            return False
            
        envelope = self.envelopes[envelope_name]
        params["actor_role"] = self.role
        
        try:
            for constraint in envelope.constraints:
                # Local deterministic evaluation
                if not eval(constraint, {"__builtins__": None}, params):
                    return False
            return True
        except:
            return False

    def execute(self, task: str, envelope: str, params: Dict[str, Any]) -> str:
        # 1. Local Admissibility Check (ENFORCEMENT)
        if not self._validate_local(envelope, params):
            raise PermissionError(f"LOCAL_REJECTION: Command violates Law Envelope [{envelope}]. Execution halted.")

        # 2. Command Chaining (IMMUATABILITY)
        command_data = f"{self.last_hash}{task}{envelope}{json.dumps(params, sort_keys=True)}"
        current_hash = hashlib.sha256(command_data.encode()).hexdigest()
        self.last_hash = current_hash

        # 3. Package Signed Payload
        payload = {
            "api_key": self.api_key,
            "role": self.role,
            "task": task,
            "envelope": envelope,
            "params": params,
            "chain_hash": current_hash,
            "prev_hash": self.last_hash
        }
        
        # Transmission to Nexorian Gateway
        return json.dumps(payload, sort_keys=True)
