import unittest

from main import remainder


class TestRemainder(unittest.TestCase):
    def test_remainder_equal(self):
        self.assertEqual(remainder(10, 3), 1)
        self.assertEqual(remainder(9, 3), 0)
        self.assertEqual(remainder(5, 2), 1)

    def test_remainder_by_zero(self):
        with self.assertRaises(ValueError):
            remainder(10, 0)


if __name__ == "__main__":
    unittest.main()
