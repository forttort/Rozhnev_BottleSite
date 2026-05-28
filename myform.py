import json
import os
import re

from bottle import request
from routes import app

EMAIL_PATTERN = re.compile(
    r'^[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?@[A-Za-z]+(?:\.[A-Za-z]+)+$'
)

JSON_FILE = 'questions.json'


def load_data():
    if not os.path.exists(JSON_FILE):
        return {}

    with open(JSON_FILE, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            return {}
        except json.JSONDecodeError:
            return {}


def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


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

    if len(question) <= 3:
        return 'The question must contain more than 3 characters.'

    if question.isdigit():
        return 'The question must not consist only of digits.'

    data = load_data()

    if mail not in data:
        data[mail] = []

    new_record = [username, question]

    duplicate_found = False
    for record in data[mail]:
        if len(record) >= 2 and record[1] == question:
            duplicate_found = True
            break

    if not duplicate_found:
        data[mail].append(new_record)
        save_data(data)
        return 'Thanks, %s! Your question has been saved.' % username

    return 'This question has already been added for this email.'