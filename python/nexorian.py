import json
import hashlib
from typing import Dict, Any

class NexusKernel:
    """
    Python SDK v0.1.1 (Step 3: Exact Match & SDK Compliance)
    """
    def __init__(self, api_key: str, domain: str = "api.nexorian.org"):
        self.api_key = api_key
        self.domain = domain

    def execute(self, task: str, envelope: str, params: Dict[str, Any]):
        # Local Schema Enforcement (Step 3)
        if not isinstance(task, str) or not isinstance(envelope, str) or not isinstance(params, dict):
            raise ValueError("SDK_ERROR: Invalid parameter types. Must match [str, str, dict].")

        # Package payload as per Spec
        payload = {
            "task": task,
            "envelope": envelope,
            "params": params
        }
        
        # In a real environment, this would be a POST request to self.domain
        # For this execution, we return the payload for Gateway processing.
        return json.dumps(payload, sort_keys=True)
