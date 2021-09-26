import json
import requests

from settings import token

# todo: Обработка ошибок разного уровня: транспорта (легли сеть, сервер), превышение лимитов или ошибка в запросе, нужно распарсивать json
# todo: Ежедневная запись в БД
# todo: Веб-приложение/ТГ-бот
# todo: Оптимизация функций


def get_portfolio():
    # авторизация    - headers  - https://tinkoffcreditsystems.github.io/invest-openapi/auth/
    # сервера апи    - api      - https://tinkoffcreditsystems.github.io/invest-openapi/env/
    # метод Портфель - endpoint - https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/portfolio

    headers = {"Authorization": "Bearer %s" % token}
    api = 'https://api-invest.tinkoff.ru/openapi/'
    endpoint = "portfolio"
    resp = requests.get(api + endpoint, headers=headers).json()


    # print(json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=4))

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


def get_summary(portfolio, portfolio_currency, price_currency):
    portfolio_value = 0

    for tick in portfolio:
        position_name = tick['name']
        balance = tick['balance']
        one_lot_price = tick['averagePositionPrice']['value']
        one_lot_currency = tick['averagePositionPrice']['currency']
        current_dynamic_price = tick['expectedYield']['value']
        current_dynamic_currency = tick['expectedYield']['currency']
        current_all_price = float(balance) * float(one_lot_price) + current_dynamic_price

        print(f"{position_name}")
        print(f"Всего:             {balance} лотов")
        print(f"Общая цена:        {current_all_price} {one_lot_currency}")
        print(f"С момента покупки: {current_dynamic_price} {current_dynamic_currency}")
        if one_lot_currency != 'RUB':
            print(f"Общая цена:        {current_all_price * price_currency[one_lot_currency]} RUB")

        print()
        print()

        if one_lot_currency == 'RUB':
            portfolio_value += current_all_price
        else:
            portfolio_value += (current_all_price * price_currency[one_lot_currency])

    print(portfolio_value + portfolio_currency['RUB'])


my_portfolio = dict(get_portfolio())["payload"]["positions"]

currency_price = {'USD': get_last_price_by_figi('BBG0013HGFT4'),
                  'EUR': get_last_price_by_figi('BBG0013HJJ31')}

get_summary(my_portfolio, get_portfolio_currency(), currency_price)





