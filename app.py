from bottle import run

from routes import app
import myform

if __name__ == "__main__":
    run(app=app, host="localhost", port=8080, debug=True)
