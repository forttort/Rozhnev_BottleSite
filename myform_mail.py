import re


DOMAIN_LABEL = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])"
EMAIL_PATTERN = re.compile(
    rf"^(?!.*\.\.)[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?@"
    rf"(?:{DOMAIN_LABEL}\.)+[A-Za-z]{{2,}}$"
)


def is_valid_email(mail):
    if not isinstance(mail, str) or not mail or not mail.isascii():
        return False

    return EMAIL_PATTERN.fullmatch(mail) is not None
