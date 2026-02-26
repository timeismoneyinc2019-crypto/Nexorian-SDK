# Nexorian API & SDK Documentation (v1.0.0)

## Overview
Nexorian provides a deterministic interface for mission-critical AI governance. All interactions pass through the Admissibility Gate before being recorded in the Deterministic Audit Ledger.

## 1. Class: `NexusKernel`
Main entry point for orchestration.

### Constructor: `__init__(api_key, role, provider="local", **kwargs)`
- `api_key`: Institutional API key.
- `role`: Actor role (`ADMIN`, `OPERATOR`, `SANDBOX`).
- `provider`: Connection type (`local` or `remote`).

### Method: `execute(task, envelope, params)`
Evaluates a task against a Law Envelope.
- **Parameters**: 
  - `task` (str): Descriptive label for the action.
  - `envelope` (str): The Law Envelope ID to enforce (e.g., `FINRA_CT_09`).
  - `params` (Dict): The operational parameters to be validated.
- **Returns**: `bool` (True if approved).
- **Raises**: `PermissionError` (If Vetoed).

## 2. Governance Response Codes
| Code | Meaning | Action |
| :--- | :--- | :--- |
| `PROVEN` | Command matches Law Envelope | EXECUTE |
| `VETO` | Command violates constraints | HALT |
| `STASIS` | System in lockdown (Threshold breach) | LOCK |

## 3. Sample Integration (Python)
```python
import nexorian

kernel = nexorian.NexusKernel("API_KEY", role="OPERATOR")
kernel.execute("DATA_TRANSFER", "SEC_G7", {"vol": 500, "limit": 1000})
```

## 4. Cryptographic Verification
The SDK provides utilities in `nexorian.utils` for verifying the integrity of log files offline using SHA3-256 chaining.
