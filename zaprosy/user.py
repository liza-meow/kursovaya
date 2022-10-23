from flask import Blueprint, render_template,request,session

from in_db import use_roots, model

zaprosy = Blueprint('zaprosy', __name__, template_folder='templates', static_folder='static')


@zaprosy.route('/')
def index():
    return 'zaprosy'


@zaprosy.route("/info")
@use_roots
def info():
    return render_template('redirect.html')


@zaprosy.route('info/ym_info', methods=["POST", "GET"])
@use_roots
def ym_info():
        if request.method == "POST":
            month = request.form.get("month", None)
            year = request.form.get("year", None)
            if not year or not month or (year.isdigit() is False or month.isdigit() is False):
                return render_template("uncorrect_info.html")
            result = model(name="ym_info", year=year, month=month)[0]
            months = model(name="ym_info", year=year, month=month)[1]
            return render_template('result1.html', items=result, year=year, month=months)
        else:
            return render_template('ym_info.html')


@zaprosy.route('info/days_info', methods=["POST", "GET"])
@use_roots
def days_info():
        if request.method == "POST":
            days = request.form.get("days", None)
            if not days or days.isdigit() is False:
                return render_template("uncorrect_info.html")
            result = model(name="days_info", days=days)
            return render_template("result2.html", items=result, day=days)
        else:
            return render_template('days_info.html')






