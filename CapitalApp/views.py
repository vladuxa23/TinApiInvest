import json
import os

from flask import render_template, request, jsonify

import CapitalApp.rest_wrapper
from CapitalApp import flask_app
from CapitalApp.forms import NewCreditForm, NewDepositForm
from CapitalApp.handlers import *

INSTRUMENT_TYPE = {"stock": "Акции",
                   "bond": "Облигации",
                   "etf": "Фонды",
                   "currency": "Валюта"}


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
        currency_price = {'USD': CapitalApp.rest_wrapper.get_last_price_by_figi(
                              'BBG0013HGFT4'),
                          'EUR': CapitalApp.rest_wrapper.get_last_price_by_figi(
                              'BBG0013HJJ31')}
        portfolio_summary = get_summary(portfolio, currency_price)

        update_portfolio_data_in_db(portfolio)

        return render_template('portfolio.html',
                               title='Инвестиции',
                               content=portfolio_summary,
                               instrument_type=INSTRUMENT_TYPE)
    else:
        return render_template('portfolio.html',
                               title='Инвестиции',
                               content=portfolio["resp"],
                               instrument_type=INSTRUMENT_TYPE)


@flask_app.route('/refresh-portfolio')
def refresh_portfolio():

    portfolio = CapitalApp.rest_wrapper.get_portfolio()

    if portfolio["status"]:
        portfolio = portfolio["resp"]["payload"]["positions"]
        # currency_price = {'USD': CapitalApp.rest_wrapper.get_last_price_by_figi(
        #                       'BBG0013HGFT4'),
        #                   'EUR': CapitalApp.rest_wrapper.get_last_price_by_figi(
        #                       'BBG0013HJJ31')}
        portfolio_summary = get_summary(portfolio,
                                        CapitalApp.rest_wrapper
                                        .get_portfolio_currency())
        return json.dumps({'success': True,
                           'result': portfolio_summary["total_portfolio_cost"]}), 200
    else:
        return render_template('portfolio.html',
                               title='Инвестиции',
                               content=portfolio["resp"])


@flask_app.route('/deposits')
def deposits_page():
    deposits_list = db.session.query(Deposits).all()
    deposit_form = NewDepositForm()

    return render_template('deposits.html',
                           title='Вклады',
                           deposit_form=deposit_form,
                           deposits_list=deposits_list)


@flask_app.route('/credits')
def credits_page():
    credits_list = db.session.query(Credits).all()
    credit_form = NewCreditForm()

    return render_template('credits.html',
                           title='Кредиты',
                           credit_form=credit_form,
                           credits_list=credits_list)


@flask_app.route('/add-credit', methods=['POST'])
def add_credit():
    # name = request.form['name']
    # date_start = request.form['date_start']
    # total_month = request.form['total_month']
    # percent = request.form['percent']
    # amount = request.form['amount']
    # amount_value = request.form['amount_value']

    try:
        db.session.add(Credits(**request.form))
        db.session.commit()
        return jsonify({'result': 'Ok'})
    except Exception as err:
        #  TODO: do something
        print(err)
        return jsonify({'error': err})


@flask_app.route('/add-deposit', methods=['POST'])
def add_deposit():

    try:
        db.session.add(Deposits(**request.form))
        db.session.commit()
        return jsonify({'result': 'Ok'})
    except Exception as err:
        #  TODO: do something
        print(err)
        return jsonify({'error': err})
