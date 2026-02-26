# Nexorian SDK: Advanced Usage Patterns

This document outlines professional orchestration patterns for the Nexorian Operational Kernel.

## 1. Multi-Layer Law Envelopes
Executing commands against nested or sequential compliance gates to ensure defense-in-depth.

```python
from nexorian import NexusKernel

kernel = NexusKernel(api_key="...", role="OPERATOR")

# Pattern: Sequential Chain Validation
def secure_operation(task, primary_gate, secondary_gate, params):
    # Layer 1: Operational Compliance
    kernel.execute(task, primary_gate, params)
    
    # Layer 2: Institutional Governance
    kernel.execute(task, secondary_gate, params)
    
    return "Consensus Reached"
```

## 2. Stateless Audit Verification
Verifying the integrity of the SHA3-256 chain without persisting to disk.

```python
from nexorian import DeterministicAuditLedger

# Verify a memory-based chain
ledger = DeterministicAuditLedger(log_path=None) 
ledger.append(1.0, "HEARTBEAT", "SYSTEM", {"status": "OK"})

if ledger.verify_integrity():
    print("Chain is cryptographically sound.")
```

## 3. Adversarial Drift Detection
Using the `NexusKernel` in Sandbox mode to probe new rulesets before upgrading to Enterprise Core.

```python
def probe_ruleset(new_ruleset_name, params):
    sandbox = NexusKernel(api_key="SANDBOX_KEY", role="SANDBOX")
    try:
        sandbox.execute("PROBE", new_ruleset_name, params)
    except PermissionError:
        return "DRIFT_DETECTED: Policy is too restrictive."
```

## 4. Hardware-ID Binding Simulation
While the SDK runs in user-space, you can anchor executions to specific hardware identifiers in the `params` set for later core-side verification.

```python
params = {
    "hw_id": get_system_uuid(),
    "nonce": generate_secure_nonce(),
    "epoch": current_epoch()
}
kernel.execute("SENSITIVE_TASK", "CORE_GENESIS", params)
```
