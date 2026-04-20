from bottle import Bottle, template, static_file

PRODUCTS = [
    {
        "name": "Кашемировое пальто",
        "description": "Культовое пальто от Hugo.",
        "price": "27 900 ₽",
        "tag": "Новинка",
        "image": "coat.png",
    },
    {
        "name": "Джинсовая куртка",
        "description": "Дерзкая куртка от PP.",
        "price": "11 500 ₽",
        "tag": "Хит",
        "image": "denim.png",
    },
    {
        "name": "Кардиган",
        "description": "Женственный кардиган от Chanel.",
        "price": "8 900 ₽",
        "image": "cardigan.png",
    },
    {
        "name": "Платье",
        "description": "Минималистичное чёрное платье  .",
        "price": "9 400 ₽",
        "image": "dress.png",
    },
    {
        "name": "Сумка-тоут",
        "description": "Плотная кожа, контрастные строчки, формат А4.",
        "price": "13 200 ₽",
        "image": "bag.png",
    },
    {
        "name": "Шарф",
        "description": "Шелковый шарф.",
        "price": "4 300 ₽",
        "image": "scarf.png",
    },
]

app = Bottle()


def render_home():
    return template("index", products=PRODUCTS)


@app.route("/")
def home():
    return render_home()


@app.get("/home")
def home_alias():
    return render_home()


@app.route("/about")
def about():
    return template("about")


@app.route("/contact")
def contact():
    return template("contact")


@app.route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="static")
