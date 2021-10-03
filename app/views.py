import json
import os

from flask import url_for, redirect, render_template, flash, g, session
from app import flask_app, db
from app.handlers import *


@flask_app.route('/')
def index():
    if not os.path.exists('app/capital.db'):
        print("БД создана")
        db.create_all()

    portfolio = app.rest_wrapper.get_portfolio()

    if portfolio["status"]:

        portfolio = portfolio["resp"]["payload"]["positions"]
        currency_price = {'USD': app.rest_wrapper.get_last_price_by_figi('BBG0013HGFT4'),
                          'EUR': app.rest_wrapper.get_last_price_by_figi('BBG0013HJJ31')}
        portfolio_summary = get_summary(portfolio, app.rest_wrapper.get_portfolio_currency(), currency_price)
        # return json.dumps(portfolio_summary, ensure_ascii=False)
        return render_template('index.html', title='Главная', content=portfolio_summary)
    else:
        # return json.dumps(portfolio["resp"], ensure_ascii=False)
        return render_template('index.html', title='Главная', content=portfolio["resp"])
