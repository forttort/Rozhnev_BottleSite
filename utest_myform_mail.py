import unittest

from myform_mail import is_valid_email


class MailFormTest(unittest.TestCase):
    def test_incorrect_email_list(self):
        list_mail_uncor = [
            "",
            "1",
            "m1@",
            "@mail.ru",
            "mail.ru",
            "m1@mail",
            "m1@m.ru",
            "m1@mail.r",
            "m1@mail..ru",
            ".m1@mail.ru",
            "m1.@mail.ru",
            "m1@-mail.ru",
            "m1@mail-.ru",
            "m1 mail@mail.ru",
            "m1@ma_il.ru",
        ]

        for mail in list_mail_uncor:
            with self.subTest(mail=mail):
                self.assertFalse(is_valid_email(mail))

    def test_correct_email_list(self):
        list_mail_cor = [
            "m.m@mail.ru",
            "m1@gmail.com",
            "user.name@example.org",
            "student-01@test-domain.ru",
            "first_last@mail.co",
            "a+b@domain.info",
            "u123@sub.mail.ru",
            "USER2026@EXAMPLE.COM",
        ]

        for mail in list_mail_cor:
            with self.subTest(mail=mail):
                self.assertTrue(is_valid_email(mail))


if __name__ == "__main__":
    unittest.main()
