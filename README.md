# Nexorian SDK Repository (Public)
## Client Interfaces & Integration Contracts

### 1. Contents
- `python/nexorian.py`: Pure interface class for kernel execution.
- `manifest.json`: Cryptographic integrity manifest.

### 2. Integration Procedure
1. Import the `NexusKernel` class.
2. Initialize with a valid API key (NEX-...).
3. Wrap all calls in a Deterministic Governance envelope.

### 3. Verification
Verify the SDK integrity via `python/nexorian.py.sha256`.

---
*INTERFACES ONLY. NO ENFORCEMENT LOGIC.*
