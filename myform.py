from bottle import request
from myform_mail import is_valid_email
from routes import app

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

    if not is_valid_email(mail):
        return 'Please enter a valid email address.'

    questions[mail] = [username, question]

    return 'Thanks, %s! The answer will be sent to the mail %s' % (username, mail)
