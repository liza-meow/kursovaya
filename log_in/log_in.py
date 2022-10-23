from flask import Blueprint, render_template, request, session, redirect, url_for

from in_db import compare

log = Blueprint('log_in', __name__, template_folder='templates', static_folder='static')


@log.route('/', methods=["POST", "GET"])
def log_in():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["pass"]
        role = compare(login, password)
        if role is False:
            title = "Неверный логин или пароль"
            return render_template("log_in.html", title=title)
        else:
            session["login"] = login
            session["role"] = role
            return redirect(url_for("menu"))
    else:
        return render_template("log_in.html")
