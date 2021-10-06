
import os

from flask import render_template

import CapitalApp.rest_wrapper
from CapitalApp import flask_app, db
from CapitalApp.handlers import *


@flask_app.route('/')
def index():
    if not os.path.exists('CapitalApp/capital.db'):
        print("БД создана")
        db.create_all()

    return render_template('index.html', title='Главная')


@flask_app.route('/stock-portfolio')
def stock_portfolio():

    portfolio = CapitalApp.rest_wrapper.get_portfolio()

    if portfolio["status"]:
        portfolio = portfolio["resp"]["payload"]["positions"]
        currency_price = {'USD': CapitalApp.rest_wrapper.get_last_price_by_figi('BBG0013HGFT4'),
                          'EUR': CapitalApp.rest_wrapper.get_last_price_by_figi('BBG0013HJJ31')}
        portfolio_summary = get_summary(portfolio, CapitalApp.rest_wrapper.get_portfolio_currency(), currency_price)

        return render_template('portfolio.html', title='Инвестиции', content=portfolio_summary)
    else:
        return render_template('portfolio.html', title='Инвестиции', content=portfolio["resp"])
