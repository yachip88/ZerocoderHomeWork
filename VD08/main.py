import requests
from flask import Flask, render_template

app = Flask(__name__)


def get_quote():
    try:
        data = requests.get("https://zenquotes.io/api/random", timeout=15).json()
        return data[0]["q"], data[0]["a"]
    except Exception:
        data = requests.get("https://quoteslate.vercel.app/api/quotes/random", timeout=15).json()
        return data.get("quote") or data.get("content"), data.get("author")


@app.route("/")
def index():
    quote, author = get_quote()
    return render_template("index.html", quote=quote, author=author)


if __name__ == "__main__":
    app.run(debug=True)
