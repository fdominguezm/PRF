import unittest
from rlwe.rlwe import RLWE

class TestRLWE(unittest.TestCase):
    def setUp(self):
        self.rlwe = RLWE(256, 12289, 3.2)  # Example parameters

    def test_generate_sample(self):
        a, b = self.rlwe.generate_sample()
        self.assertEqual(len(a), 256)
        self.assertEqual(len(b), 256)

    def test_decision_rlwe(self):
        # Test decision RLWE
        pass

    def test_search_rlwe(self):
        # Test search RLWE
        pass

if __name__ == '__main__':
    unittest.main()
