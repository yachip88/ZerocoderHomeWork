from datetime import datetime

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return f"<h1>Сейчас: {now}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
