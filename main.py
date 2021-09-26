import requests
import json
from settings import token

def get_portfolio():
    # авторизация https://tinkoffcreditsystems.github.io/invest-openapi/auth/
    headers = {"Authorization": "Bearer %s" % token}
    # урл до серверов апи https://tinkoffcreditsystems.github.io/invest-openapi/env/
    api = 'https://api-invest.tinkoff.ru/openapi/'
    # метод Портфель https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/#/portfolio
    endpoint = "portfolio"
    resp = requests.get(api + endpoint, headers=headers).json()
    # todo: Обработка ошибок разного уровня: транспорта (легли сеть, сервер), превышение лимитов или ошибка в запросе, нужно распарсивать json
    print(json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=4))
    return resp

my_portfolio = dict(get_portfolio())["payload"]["positions"]

for tick in my_portfolio:
    print(tick)
    # print(f"{tick['name']} Всего {tick['balance']} стоимостью по {tick['averagePositionPrice']['value']} {tick['averagePositionPrice']['currency']}")



