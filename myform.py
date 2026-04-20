import re
import pdb

from bottle import request
from routes import app

EMAIL_PATTERN = re.compile(
    r'^[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?@[A-Za-z]+(?:\.[A-Za-z]+)+$'
)

questions = {}


@app.post('/home')
def my_form():
    username = request.forms.get('USERNAME', '').strip()
    question = request.forms.get('QUEST', '').strip()
    mail = request.forms.get('ADRESS', '').strip()

    missing_fields = []
    if not username:
        missing_fields.append('USERNAME')
    if not question:
        missing_fields.append('QUEST')
    if not mail:
        missing_fields.append('ADRESS')

    if missing_fields:
        return 'Please fill in all fields: %s.' % ', '.join(missing_fields)

    if not mail.isascii() or not EMAIL_PATTERN.fullmatch(mail):
        return 'Please enter a valid email address.'

    questions[mail] = [username, question]

    pdb.set_trace()

    return 'Thanks, %s! The answer will be sent to the mail %s' % (username, mail)