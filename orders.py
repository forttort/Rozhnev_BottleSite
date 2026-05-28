import json
import re
from datetime import date, datetime
from pathlib import Path

from bottle import redirect, request, template

from routes import app


# JSON лежит рядом с модулем, поэтому путь не зависит от директории запуска.
DATA_FILE = Path(__file__).with_name("orders.json")
ORDER_NUMBER_ALLOWED_PATTERN = re.compile(r"^[A-Za-zА-Яа-яЁё0-9-]+$")
DESCRIPTION_ALLOWED_PATTERN = re.compile(r"^[A-Za-zА-Яа-яЁё0-9\s.,!?;:()№+\"'/-]+$")
PHONE_PATTERN = re.compile(r"^\+7\d{10}$")
MIN_ORDER_DATE = date(2024, 1, 1)


def load_orders():
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return []

    if isinstance(data, list):
        return [order for order in data if isinstance(order, dict)]
    return []


def save_orders(orders):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)


def parse_order_date(value):
    return datetime.strptime(value, "%d.%m.%Y").date()


def is_valid_order_date(value, today=None):
    today = today or date.today()
    try:
        order_date = parse_order_date(value)
    except ValueError:
        return False

    return MIN_ORDER_DATE <= order_date <= today


def normalize_phone(value):
    digits = re.sub(r"\D", "", value)
    if len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    if len(digits) == 11 and digits.startswith("7"):
        return "+" + digits
    return value.strip()


def is_valid_phone(value):
    return bool(PHONE_PATTERN.fullmatch(normalize_phone(value)))


def sort_orders(orders):
    def order_key(order):
        try:
            return parse_order_date(order.get("date", "01.01.1900"))
        except ValueError:
            return date.min

    return sorted(orders, key=order_key, reverse=True)


def validate_order(form_data, existing_orders=None, today=None):
    # Валидация вынесена отдельно, чтобы ее можно было проверять unit-тестами.
    existing_orders = existing_orders or []
    errors = {}

    number = form_data.get("number", "").strip()
    description = form_data.get("description", "").strip()
    order_date = form_data.get("date", "").strip()
    phone = form_data.get("phone", "").strip()

    def add_error(field, message):
        errors.setdefault(field, []).append(message)

    if not number:
        add_error("number", "Укажите номер заказа.")
    else:
        if len(number) < 3:
            add_error("number", "Номер должен быть не короче 3 символов.")
        if len(number) > 20:
            add_error("number", "Номер должен быть не длиннее 20 символов.")
        if re.search(r"\s", number):
            add_error("number", "Номер не должен содержать пробелы.")
        if not ORDER_NUMBER_ALLOWED_PATTERN.fullmatch(number):
            add_error("number", "В номере разрешены только буквы, цифры и дефис.")
        if not any(char.isalpha() for char in number):
            add_error("number", "В номере заказа должна быть хотя бы одна буква.")
        if not any(char.isdigit() for char in number):
            add_error("number", "В номере заказа должна быть хотя бы одна цифра.")
        if number.startswith("-") or number.endswith("-"):
            add_error("number", "Номер не должен начинаться или заканчиваться дефисом.")
        if "--" in number:
            add_error("number", "Номер не должен содержать два дефиса подряд.")
        if any(order.get("number", "").lower() == number.lower() for order in existing_orders):
            add_error("number", "Заказ с таким номером уже есть в списке.")

    if not description:
        add_error("description", "Заполните описание заказа.")
    else:
        if len(description) < 10:
            add_error("description", "Описание должно быть не короче 10 символов.")
        if len(description) > 300:
            add_error("description", "Описание должно быть не длиннее 300 символов.")
        if description.isdigit():
            add_error("description", "Описание не может состоять только из цифр.")
        if not any(char.isalpha() for char in description):
            add_error("description", "Описание должно содержать хотя бы одну букву.")
        if len(description.split()) < 2:
            add_error("description", "Описание должно содержать минимум два слова.")
        if re.search(r"[\x00-\x1f\x7f]", description):
            add_error("description", "Описание не должно содержать управляющие символы.")
        if re.search(r"https?://|www\.", description, re.IGNORECASE):
            add_error("description", "Описание не должно содержать ссылки.")
        if re.search(r"(.)\1{5,}", description):
            add_error("description", "Описание не должно содержать один символ более 5 раз подряд.")
        if "<" in description or ">" in description:
            add_error("description", "Описание не должно содержать HTML-теги.")
        if not DESCRIPTION_ALLOWED_PATTERN.fullmatch(description):
            add_error("description", "Описание содержит запрещенные символы.")

    if not order_date:
        add_error("date", "Укажите дату заказа.")
    else:
        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", order_date):
            add_error("date", "Дата должна быть в формате ДД.ММ.ГГГГ.")
        else:
            try:
                parsed_date = parse_order_date(order_date)
            except ValueError:
                add_error("date", "Дата должна быть реальной календарной датой.")
            else:
                current_day = today or date.today()
                if parsed_date < MIN_ORDER_DATE:
                    add_error("date", "Дата не должна быть раньше 01.01.2024.")
                if parsed_date > current_day:
                    add_error("date", "Дата не должна быть позже текущего дня.")

    if not phone:
        add_error("phone", "Укажите телефон покупателя.")
    else:
        if re.search(r"[A-Za-zА-Яа-яЁё]", phone):
            add_error("phone", "Телефон не должен содержать буквы.")
        if re.search(r"[<>\"'`{}[\]|\\\\]", phone):
            add_error("phone", "Телефон содержит запрещенные символы.")
        if len(re.sub(r"\D", "", phone)) != 11:
            add_error("phone", "Телефон должен содержать ровно 11 цифр.")
        if not is_valid_phone(phone):
            add_error("phone", "Телефон должен быть российским: +7 (999) 123-45-67 или 89991234567.")

    return errors


def get_form_data():
    # getunicode сохраняет русские символы при отправке формы Bottle.
    return {
        "number": request.forms.getunicode("number", "").strip(),
        "description": request.forms.getunicode("description", "").strip(),
        "date": request.forms.getunicode("date", "").strip(),
        "phone": request.forms.getunicode("phone", "").strip(),
    }


def render_orders(form_data=None, errors=None, success=False):
    return template(
        "orders",
        orders=sort_orders(load_orders()),
        form_data=form_data or {},
        errors=errors or {},
        success=success,
    )


@app.get("/orders")
def orders_page():
    return render_orders(success=request.query.get("created") == "1")


@app.post("/orders")
def add_order():
    form_data = get_form_data()
    orders = load_orders()
    errors = validate_order(form_data, existing_orders=orders)

    if errors:
        return template(
            "orders",
            orders=sort_orders(orders),
            form_data=form_data,
            errors=errors,
            success=False,
        )

    orders.append(
        {
            "number": form_data["number"],
            "description": form_data["description"],
            "date": form_data["date"],
            "phone": normalize_phone(form_data["phone"]),
        }
    )
    save_orders(sort_orders(orders))

    return redirect("/orders?created=1")
