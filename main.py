from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User

import uuid
import hashlib
import random
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("Index.html")
    elif request.method == "POST":
        contact_name = request.form.get("contact-name")
        contact_email = request.form.get("contact-email")
        contact_message = request.form.get("contact-message")

        response = make_response(render_template("success.html", name=contact_name, email=contact_email, message=contact_message))

        response.set_cookie("user_name", contact_name)
        response.set_cookie("user_email", contact_email)
        response.set_cookie("user_message", contact_message)

        return response


@app.route("/story", methods=['GET', 'POST'])
def story():
    if request.method == "GET":
        user_name = request.cookies.get("user_name")
        return render_template("story.html", name=user_name)


@app.route("/projects", methods=['GET', 'POST'])
def projects():
    return render_template("projects.html")


@app.route("/game", methods=['GET', 'POST'])
def game():
    if request.method == "GET":
        contact_name = request.cookies.get("contact-name")
        contact_email = request.cookies.get("contact-email")
        random_number = request.cookies.get("random_number")

        response = make_response(render_template("game.html", name=contact_name, email=contact_email, message="Guess The Number"))

        user = request.cookies.get("session_token")

        if not user:
            return render_template("gamelog.html")
        else:
            if not random_number:
                random_number = random.randint(1, 30)
                response.set_cookie("random_number", str(random_number))
            return response
    else:
        guess = int(request.form.get("guess"))

        secret_num = int(request.cookies.get("random_number"))
        contact_name = request.cookies.get("contact-name")
        contact_email = request.cookies.get("contact-email")

        if guess == secret_num:
            message = "Congratulations! You've guessed the number!"
            response = make_response(render_template("gamefin.html", name=contact_name, email=contact_email, message=message, num=f"It is: {secret_num}"))
            secret_num = random.randint(1, 30)
            response.set_cookie("random_number", str(secret_num))
            return response
        elif guess > secret_num:
            message = "Secret number is some smaller"
            response = make_response(render_template("game.html", name=contact_name, email=contact_email, message=message, num=""))
            return response
        else:
            message = "Secret number is some bigger"
            response = make_response(render_template("game.html", name=contact_name, email=contact_email, message=message, num=""))
            return response


@app.route("/gamelog", methods=['GET', 'POST'])
def gamelog():
    if request.method == "GET":
        return render_template("gamelog.html")

    elif request.method == "POST":
        contact_name = request.form.get("contact-name")
        contact_email = request.form.get("contact-email")
        contact_pass = request.form.get("contact-pass")
        session_token = request.cookies.get("session_token")

        user = User.fetch_one(query=["session_token", "==", session_token])
        hashed_pass = hashlib.sha256(contact_pass.encode()).hexdigest()

        if not user:
            user = User(name=contact_name, email=contact_email, password=hashed_pass)
            user.create()
            response = redirect(url_for("game"))
            session_token = str(uuid.uuid4())
            User.edit(obj_id=user.id, session_token=session_token)
            response.set_cookie("session_token", session_token)
            return response
        else:
            if hashed_pass != user.password:
                return make_response(render_template("gamelog.html", message="Wrong password! Try again."))
            elif hashed_pass == user.password:
                session_token = str(uuid.uuid4())
                User.edit(obj_id=user.id, session_token=session_token)

                response = redirect(url_for("game"))

                response.set_cookie("session_token", session_token, httponly=True, secure=True, expires=10)
                response.set_cookie("contact-name", contact_name)
                response.set_cookie("contact-email", contact_email)

                return response





if __name__ == "__main__":
    app.run(debug=True)
