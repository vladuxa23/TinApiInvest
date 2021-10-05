import json
import traceback
import requests
from settings import token
from bs4 import BeautifulSoup


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


def get_ticker_image_link(ticker):
    url = f"https://www.tinkoff.ru/invest/stocks/{ticker}/"
    return None