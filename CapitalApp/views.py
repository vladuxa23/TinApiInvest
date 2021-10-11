import json
import os

from flask import render_template

import CapitalApp.rest_wrapper
from CapitalApp import flask_app, db
from CapitalApp.handlers import *

INSTRUMENT_TYPE = {"stock": "Акции", "bond": "Облигации", "etf": "Фонды", "currency": "Валюта"}


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

        return render_template('portfolio.html', title='Инвестиции',
                               content=portfolio_summary, instrument_type=INSTRUMENT_TYPE)
    else:
        return render_template('portfolio.html', title='Инвестиции',
                               content=portfolio["resp"], instrument_type=INSTRUMENT_TYPE)


@flask_app.route('/refresh-portfolio')
def refresh_portfolio():

    portfolio = CapitalApp.rest_wrapper.get_portfolio()

    if portfolio["status"]:
        portfolio = portfolio["resp"]["payload"]["positions"]
        currency_price = {'USD': CapitalApp.rest_wrapper.get_last_price_by_figi('BBG0013HGFT4'),
                          'EUR': CapitalApp.rest_wrapper.get_last_price_by_figi('BBG0013HJJ31')}
        portfolio_summary = get_summary(portfolio, CapitalApp.rest_wrapper.get_portfolio_currency(), currency_price)
        return json.dumps({'success': True, 'result': portfolio_summary["total_portfolio_cost"]}), 200
        # return make_response({'success': True, 'result': portfolio_summary["total_portfolio_cost"]}, 200)
    else:
        return render_template('portfolio.html', title='Инвестиции', content=portfolio["resp"])


@flask_app.route('/summary')
def summary_page():
    return render_template('summary.html', title='Сводка')


@flask_app.route('/credits')
def credits_page():
    return render_template('credits.html', title='Сводка')
