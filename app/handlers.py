import requests
from pprint import pprint
import app.rest_wrapper

# todo: Обработка ошибок разного уровня: транспорта (легли сеть, сервер), превышение лимитов или ошибка в запросе,
#  нужно распарсивать json
# todo: Ежедневная запись в БД
# todo: Веб-приложение/ТГ-бот
# todo: Оптимизация функций


def get_summary(portfolio, portfolio_currency, price_currency):
    portfolio_value = 0
    portfolio_dict = dict()
    for tick in portfolio:
        position_name = tick['name']
        balance = tick['balance']
        one_lot_price = tick['averagePositionPrice']['value']
        one_lot_currency = tick['averagePositionPrice']['currency']
        current_dynamic_price = tick['expectedYield']['value']
        current_dynamic_currency = tick['expectedYield']['currency']
        current_all_price = float(balance) * float(one_lot_price) + current_dynamic_price

        if one_lot_currency != 'RUB':
            current_all_price = current_all_price * price_currency[one_lot_currency]

        portfolio_dict.update({position_name: {"value": balance,
                                               "total_cost": current_all_price,
                                               "total_cost_currency": one_lot_currency,
                                               "current_dynamic_price": current_dynamic_price,
                                               "current_dynamic_currency": current_dynamic_currency}})
        # print(f"{position_name}")
        # print(f"Всего:             {balance} лотов")
        # print(f"Общая цена:        {current_all_price} {one_lot_currency}")
        # print(f"С момента покупки: {current_dynamic_price} {current_dynamic_currency}")

        if one_lot_currency == 'RUB':
            portfolio_value += current_all_price
        else:
            portfolio_value += (current_all_price * price_currency[one_lot_currency])
    portfolio_dict.update({"total_portfolio_cost": portfolio_value})

    return portfolio_dict


