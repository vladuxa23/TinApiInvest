from .rest_wrapper import get_ticker_image_link_online, get_portfolio_currency


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
        instrument_type = tick['instrumentType'].lower()
        one_lot_price = tick['averagePositionPrice']['value']
        one_lot_currency = tick['averagePositionPrice']['currency']
        current_dynamic_price = tick['expectedYield']['value']
        current_dynamic_currency = tick['expectedYield']['currency']
        current_all_price = float(balance) * float(one_lot_price) + current_dynamic_price
        ticker_img = get_ticker_image_link_online(tick['instrumentType'], tick['ticker'])

        if one_lot_currency != 'RUB':
            current_all_price = current_all_price * price_currency[one_lot_currency]

        if instrument_type not in portfolio_dict:
            portfolio_dict.update({instrument_type: {}})

        portfolio_dict[instrument_type].update({position_name: {"value": balance,
                                                                 "total_cost": round(current_all_price, 2), # Подсчёт всего!!!
                                                                 "total_cost_currency": one_lot_currency,
                                                                 "current_dynamic_price": round(current_dynamic_price, 2), #
                                                                 "current_dynamic_currency": current_dynamic_currency,
                                                                 "ticker_img": ticker_img}})

        portfolio_value += current_all_price
    portfolio_value += get_portfolio_currency()["RUB"]  # Добавляем рубли из портфеля

    portfolio_dict.update({"total_portfolio_cost": round(portfolio_value, 2)})

    return portfolio_dict
