from bottle import run

from routes import app

if __name__ == "__main__":
    run(app=app, host="localhost", port=8080, debug=True)
