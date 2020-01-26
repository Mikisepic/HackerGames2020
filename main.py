from flask import Flask, render_template, request, make_response, redirect, url_for
import json

app = Flask(__name__)


@app.route("/")
def index():
    with open('universities.json', 'r', encoding="utf8") as universities:
        data = json.load(universities)
        return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
