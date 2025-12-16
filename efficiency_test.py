import unittest

class TestPRNG(unittest.TestCase):

    def setUp(self):
        self.prng = self.PRNG_CLASS()

    def test_initial_state(self):
        self.assertEqual(self.prng.state, b"\x00" * 32)
        self.assertEqual(self.prng.counter, 0)

    def test_output_length(self):
        lengths = [1, 16, 32, 64, 128]
        for length in lengths:
            output = self.prng.next(length)
            self.assertEqual(len(output), length)
    
    def test_repeatability_without_refresh(self):
        rng1 = self.PRNG_CLASS()
        rng2 = self.PRNG_CLASS()
        self.assertNotEqual(rng1.next(32), rng2.next(32))

    def test_refresh_changes_output(self):
        output_before = self.prng.next(32)
        output_after = self.prng.next(32)
        self.assertNotEqual(output_before, output_after)

    def test_refresh_with_entropy(self):
        output_before = self.prng.next(32)
        entropy = b"some_entropy_data"
        self.prng.refresh(entropy)
        output_after = self.prng.next(32)
        self.assertNotEqual(output_before, output_after)

