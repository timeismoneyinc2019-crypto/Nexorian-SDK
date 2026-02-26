# Nexorian Operational SDK (v1.0.0)

Professional-grade orchestration and governance for Deterministic AI kernels.

## 📦 Installation
```bash
pip install .
```

## 🚀 Sandbox Operational Demo
The SDK provides a built-in `LocalProvider` for sandbox testing and reproducibility.

```python
from nexorian import NexusKernel

# Initialize an operational sandbox kernel
kernel = NexusKernel(api_key="SANDBOX_KEY", role="SANDBOX")

# Execute a task governed by the FINRA_CT_09 Law Envelope
try:
    kernel.execute(
        task="DATA_EGRESS",
        envelope="FINRA_CT_09",
        params={"epoch": 0.5, "epoch_limit": 1.0}
    )
    print("Governance Check: PROVEN. Instruction Sent.")
except PermissionError as e:
    print(f"Governance Check: VETOED. {e}")
```

## 🛡️ SHA-256 Verification Guide (MANDATORY)
To ensure the integrity of the project's artifacts (Whitepaper, Thesis, Logs), follow these steps:

1. **Download Artifacts**: Retrieve the desired file from the [Nexorian-Audit](https://github.com/timeismoneyinc2019-crypto/Nexorian-Audit) repository.
2. **Verify against Manifest**:
   ```bash
   # Windows (PowerShell)
   (Get-FileHash -Path .\FILENAME -Algorithm SHA256).Hash.ToLower()
   
   # Linux/macOS
   sha256sum FILENAME
   ```
3. **Cross-Reference**: Compare the resulting hash with the entries in `manifest.json`.

## 🧪 Documentation & Usage
- **Advanced Patterns**: See `docs/USAGE_PATTERNS.md` for institutional orchestration.
- **Reproducibility**: See `tests/` for verifiable integration examples.

## ⚖️ Governance Standards
This SDK adheres to the [Nexorian Calculus of Deterministic Governance](https://nexorian.org). No probabilistic enforcements are used in the core kernel.
