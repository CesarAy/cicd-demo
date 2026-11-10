"""Run with: python3 -m unittest discover -v"""

import unittest

from calculator import add, divide, multiply, subtract


class CalculatorTests(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)

    def test_add_zero(self):
        self.assertEqual(add(7, 0), 7)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_multiply(self):
        self.assertEqual(multiply(6, 7), 42)

    def test_multiply_by_zero(self):
        self.assertEqual(multiply(9, 0), 0)

    def test_divide(self):
        self.assertEqual(divide(10, 4), 2.5)

    def test_divide_negative_number(self):
        self.assertEqual(divide(-12, 3), -4)

    def test_divide_by_zero(self):
        with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
            divide(10, 0)

    def test_multiply_negative_numbers(self):
        self.assertEqual(multiply(-3, -4), 12)


if __name__ == "__main__":
    unittest.main()
