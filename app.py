import json

from flask import Flask, render_template, session

from zaprosy.user import zaprosy
from log_in.log_in import log
from basket.basket import basket_app


app = Flask(__name__)
app.secret_key = "kursovaya"
app.config["ACCESS_CONFIG"] = json.load(open('configs/acces.json'))
app.register_blueprint(zaprosy, url_prefix='/zaprosy')
app.register_blueprint(log, url_prefix='/log_in')
app.register_blueprint(basket_app, url_prefix='/basket')


@app.route("/")
def main_page():
    # Начальная страница входа в приложение
    return render_template("main_page.html")


@app.route('/menu')
def menu():
    if "login" in session:
        return render_template('menu.html', role=session['role'])
    else:
        return render_template("unlogin.html")


@app.route('/exit')
def exit_app():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(port=9003)
