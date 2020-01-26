from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    with open('universities.json', 'r') as universities:
        data = json.load(universities)
        return render_template('index.html', data=data)

@app.route("/landing")
def landing():
    return render_template('landing.html')

if __name__ == "__main__":
    app.run(debug=True)
