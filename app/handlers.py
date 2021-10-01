import requests
from pprint import pprint
import rest_wrapper
from models import *

# todo: Обработка ошибок разного уровня: транспорта (легли сеть, сервер), превышение лимитов или ошибка в запросе,
#  нужно распарсивать json
# todo: Ежедневная запись в БД
# todo: Веб-приложение/ТГ-бот
# todo: Оптимизация функций


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


# if __name__ == '__main__':

    #
    # portfolio = rest_wrapper.get_portfolio()
    #
    # if portfolio["status"]:
    #
    #     portfolio = portfolio["resp"]["payload"]["positions"]
    #     currency_price = {'USD': rest_wrapper.get_last_price_by_figi('BBG0013HGFT4'),
    #                       'EUR': rest_wrapper.get_last_price_by_figi('BBG0013HJJ31')}
    #     get_summary(portfolio, rest_wrapper.get_portfolio_currency(), currency_price)
    # else:
    #     pprint(portfolio["resp"])
