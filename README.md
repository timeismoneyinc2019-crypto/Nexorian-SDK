# Nexorian Python SDK (Operational Kernel)

The Nexorian SDK is a high-fidelity, deterministic governance kernel designed for industrial AI orchestration. Unlike lite wrappers, the Nexorian SDK provides a complete standalone enforcement surface.

## 📦 Installation
```bash
pip install .
```

## 🚀 Quick Start (Operational Kernel)
```python
from nexorian import NexusKernel

# Initialize a standalone operational kernel
kernel = NexusKernel(api_key="YOUR_KEY", role="SANDBOX")

# Execute mission-critical logic bound by a Law Envelope
try:
    kernel.execute(
        task="INIT_SEQUENCE",
        envelope="FINRA_CT_09",
        params={"epoch": 0.1, "epoch_limit": 1.0}
    )
    print("Execution Approved & Logged.")
except PermissionError as e:
    print(f"Execution Vetoed: {e}")
```

## 🛡️ Core Features
- **Deterministic Compliance Engine (DCE)**: Real-world enforcement of Law Envelopes.
- **SHA3-256 Audit Ledger**: Immutable, cryptographically chained execution logs.
- **Zero-Trust Enforcement**: Local kernel validation before any state transition.
- **Standalone Mode**: 100% operational without remote dependencies.

## 📄 Documentation
- **[Advanced Usage Patterns](docs/USAGE_PATTERNS.md)**: Industrial-grade orchestration examples.
- **[Nexorian Official Site](https://nexorian.org)**: Governance Specs and Audit Evidence.
