import unittest
from datetime import date

from orders import is_valid_order_date, is_valid_phone, validate_order


class OrderValidationTest(unittest.TestCase):
    def test_accepts_real_order_date_in_required_format(self):
        self.assertTrue(is_valid_order_date("28.05.2026", today=date(2026, 5, 28)))

    def test_rejects_invalid_order_date(self):
        self.assertFalse(is_valid_order_date("31.02.2026", today=date(2026, 5, 28)))

    def test_accepts_russian_phone_formats(self):
        self.assertTrue(is_valid_phone("+7 (900) 123-45-67"))
        self.assertTrue(is_valid_phone("89001234567"))

    def test_rejects_invalid_phone(self):
        self.assertFalse(is_valid_phone("+1 900 123-45-67"))

    def test_collects_multiple_errors_without_exception(self):
        errors = validate_order(
            {
                "number": "--",
                "description": "123!!!!!!",
                "date": "2026-05-28",
                "phone": "phone<>",
            },
            today=date(2026, 5, 28),
        )

        self.assertIn("number", errors)
        self.assertIn("description", errors)
        self.assertIn("date", errors)
        self.assertIn("phone", errors)
        self.assertGreaterEqual(len(errors["number"]), 3)
        self.assertGreaterEqual(len(errors["description"]), 2)
        self.assertGreaterEqual(len(errors["phone"]), 3)

    def test_rejects_duplicate_order_number(self):
        errors = validate_order(
            {
                "number": "MN-1001",
                "description": "Пальто с доставкой курьером",
                "date": "28.05.2026",
                "phone": "+7 (900) 123-45-67",
            },
            existing_orders=[{"number": "mn-1001"}],
            today=date(2026, 5, 28),
        )

        self.assertIn("number", errors)

    def test_rejects_description_with_forbidden_content(self):
        errors = validate_order(
            {
                "number": "MN-2005",
                "description": "<script> http://bad.test",
                "date": "28.05.2026",
                "phone": "+7 (900) 123-45-67",
            },
            today=date(2026, 5, 28),
        )

        self.assertIn("description", errors)
        self.assertGreaterEqual(len(errors["description"]), 2)


if __name__ == "__main__":
    unittest.main()
