import json
import os
import traceback

import requests
from bs4 import BeautifulSoup

from settings import token
from . import db
from .models import TickerImage


def get_portfolio():
    # авторизация    - headers  - https://tinkoffcreditsystems.github.io/invest-openapi/auth/
    # сервера апи    - api      - https://tinkoffcreditsystems.github.io/invest-openapi/env/
    # метод Портфель - endpoint - https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/portfolio

    headers = {f"Authorization": f"Bearer {token}"}
    api = 'https://api-invest.tinkoff.ru/openapi/'
    endpoint = "portfolio"

    try:
        resp = requests.get(api + endpoint, headers=headers).json()
    except json.JSONDecodeError:
        resp = {"resp": traceback.format_exc(), "status": False}
        return resp

    # print(json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=4))

    if resp["status"] == "Error":
        resp = {"resp": resp, "status": False}
    else:
        resp = {"resp": resp, "status": True}

    return resp


def get_ticker_info_by_ticker(ticker):
    headers = {"Authorization": "Bearer %s" % token}
    api = 'https://api-invest.tinkoff.ru/openapi/'
    endpoint = f"market/search/by-ticker?ticker={ticker}"
    resp = requests.get(api + endpoint, headers=headers).json()

    return resp


def get_last_price_by_figi(figi, depth=1):
    headers = {"Authorization": "Bearer %s" % token}
    api = 'https://api-invest.tinkoff.ru/openapi/'
    endpoint = f"market/orderbook?figi={figi}&depth={depth}"
    resp = requests.get(api + endpoint, headers=headers).json()

    return float(resp['payload']['lastPrice'])


def get_portfolio_currency():
    headers = {"Authorization": "Bearer %s" % token}
    api = 'https://api-invest.tinkoff.ru/openapi/'
    endpoint = "portfolio/currencies"
    resp = requests.get(api + endpoint, headers=headers).json()

    currency_values = dict()
    for elem in resp["payload"]["currencies"]:
        currency_values.update({elem['currency']: elem['balance']})

    return currency_values


def get_ticker_image_link_online(instr: str, ticker: str) -> str:
    instr = instr.lower()
    ticker = ticker.lower()
    null_image = 'img/card_no_image.jpg'
    ticker_logo = f'img/{ticker}_logo_img.jpg'

    img_path = os.path.join('CapitalApp', 'static', 'img', f'{ticker}_logo_img.jpg')
    if os.path.exists(img_path):
        return ticker_logo  # не возвращаем полный путь т.к. в HTML url_for

    url = f"https://www.tinkoff.ru/invest/{instr}s/{ticker}/"
    data = requests.get(url)
    if data.status_code == 200:
        parser = BeautifulSoup(data.text, "html.parser")
        all_img = str(parser.findAll('div', class_='InvestLogo__root_2xvQS InvestLogo__root_size_xl_3AVii'))
        if len(all_img) > 10:  # защита если ссылка на изображение не найдена '[]'

            img_link = 'https:' + all_img.split('(')[1].split(')')[0]
            img = requests.get(img_link)
            # add_ticker_image_blob_to_db(img_link, ticker, img.content)
            with open(img_path, 'wb') as f:
                f.write(img.content)

            ticker_image = TickerImage(ticker, img_link, img.content)
            db.session.add(ticker_image)
            db.session.commit()

            return ticker_logo  # возвращаем все равно короткий путь т.к. в шаблоне url_for
        return null_image
    else:
        return null_image


def add_ticker_image_blob_to_db(image_link, ticker, image):
    # id = db.Column(db.Integer, primary_key=True)
    # ticker = db.Column(db.String)
    # imagelink = db.Column(db.String(255))
    # image = db.Column(db.BLOB)
    #
    # ticker_image = TickerImage(ticker=ticker, imagelink=image_link, image=image)
    # db.session.add(ticker_image)
    # db.session.commit()
    pass


