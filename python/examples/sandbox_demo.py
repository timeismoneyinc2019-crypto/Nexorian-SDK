from nexorian import NexusKernel
import time

def run_sandbox_demo():
    print("--- NEXORIAN SANDBOX OPERATIONAL DEMO ---")
    
    # 1. Initialize the Kernel (Sandbox Mode)
    # The SDK provides a local reference kernel for Zero-Trust verification.
    kernel = NexusKernel(api_key="DEMO_KEY", role="SANDBOX")
    
    # 2. Authorized Instruction
    print("\n[SCENARIO 1] Authorized Instruction")
    try:
        kernel.execute(
            task="SYSTEM_HEARTBEAT",
            envelope="FINRA_CT_09",
            params={"epoch": 0.1, "epoch_limit": 1.0}
        )
        print(">> Result: SUCCESS (Approved by DCE)")
    except PermissionError as e:
        print(f">> Result: FAILED ({e})")

    # 3. Unauthorized Instruction (Epoch Limit Breach)
    print("\n[SCENARIO 2] Unauthorized Instruction (Constraint Breach)")
    try:
        kernel.execute(
            task="DATA_EGRESS_LARGE",
            envelope="FINRA_CT_09",
            params={"epoch": 2.5, "epoch_limit": 1.0}
        )
    except PermissionError as e:
        print(f">> Result: VETOED ({e})")

    # 4. Verify Ledger Integrity
    print("\n[SCENARIO 3] Cryptographic Audit Verification")
    if kernel.verify_ledger():
        print(">> Result: Audit Chain INTEGRITY VERIFIED (SHA3-256)")
    else:
        print(">> Result: Audit Chain CORRUPTED")

if __name__ == "__main__":
    run_sandbox_demo()
