# Rozhnev BottleSite

Минималистичный лендинг магазина одежды на Bottle.

## Что внутри
- `app.py` — Bottle-приложение со списком товаров и маршрутами `/`, `/about`, `/contact`.
- `views/` — шаблоны Bottle, `static/` — стили и иллюстрации.

## Запуск
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

После запуска сайт доступен на `http://localhost:8080`.
