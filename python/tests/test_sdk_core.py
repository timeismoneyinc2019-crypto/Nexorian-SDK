import unittest
from nexorian import NexusKernel

class TestNexorianSDK(unittest.TestCase):
    def setUp(self):
        self.kernel = NexusKernel(api_key="TEST_KEY", role="SANDBOX")

    def test_initialization(self):
        self.assertEqual(self.kernel.api_key, "TEST_KEY")
        self.assertEqual(self.kernel.role, "SANDBOX")
        self.assertEqual(self.kernel.state, "IDLE")

    def test_governance_rejection(self):
        # Trigger a rejection by using a role that is too low for a restricted envelope
        # Assuming our reference kernel has a rule for FINRA_CT_09 requiring ADMIN or similar
        # In our ref kernel it evaluates params.
        with self.assertRaises(PermissionError):
            self.kernel.execute("DATA_SEND", "FINRA_CT_09", {"epoch": 10.0, "epoch_limit": 1.0})

    def test_governance_approval(self):
        # Trigger an approval
        result = self.kernel.execute("HEARTBEAT", "FINRA_CT_09", {"epoch": 0.1, "epoch_limit": 1.0})
        self.assertTrue(result)
        self.assertEqual(self.kernel.state, "IDLE")

    def test_ledger_integrity(self):
        self.kernel.execute("PROBE", "FINRA_CT_09", {"epoch": 0.2, "epoch_limit": 1.0})
        self.assertTrue(self.kernel.verify_ledger())

if __name__ == "__main__":
    unittest.main()
