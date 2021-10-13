from .rest_wrapper import get_ticker_image_link_online, get_portfolio_currency
from .models import *
import datetime


# todo: Обработка ошибок разного уровня: транспорта (легли сеть, сервер),
#  превышение лимитов или ошибка в запросе, нужно распарсивать json
# todo: Ежедневная запись в БД
# todo: Веб-приложение/ТГ-бот
# todo: Оптимизация функций


def update_portfolio_data_in_db(portfolio: list) -> tuple:
    """
    Функция добавляет записи о состоянии портфеля на текущий момент времени

    :param portfolio: список словарей текущего состояния портфеля
    :type portfolio: list

    :rtype: (bool, str)
    :return: (func result, string of result with update date)
    """

    # TODO: Не обновлять портфолио если последнее обновление было меньше часа
    #  назад

    # Перебираем словари в списке словарей
    for elem in portfolio:
        # Добавляем значение в бд, распаковывая элементы в класс Portfolio
        db.session.add(Portfolio(**elem))
    # Сохраняем состояние бд
    db.session.commit()

    return True, f'Данные успешно обновлены в ' \
                 f'{datetime.datetime.utcnow().isoformat()}'


def get_summary(portfolio: list, price_currency: dict) -> dict:
    """
    Функция переформатирует исходный список со словарями (текущее состояние 
    портфеля) в словарь словарей для отображения на странице 
    :param portfolio: список словарей текущего состояния портфеля
    :type portfolio: list 
    :param price_currency: словарь с текущей ценой на валюту в портфеле
    :type price_currency: dict
    :return: dict(instrument_type:dict(name:(dict(instrument_info))))
    """

    # Переменная для подсчёта общей стоимости портфеля
    portfolio_value = 0
    # Словарь, который будет возвращен в результате
    portfolio_dict = dict()

    # Перебираем инструменты в словаре и формируем значения для нового словаря
    for tick in portfolio:
        position_name = tick['name']
        balance = tick['balance']
        instrument_type = tick['instrumentType'].lower()
        one_lot_price = tick['averagePositionPrice']['value']
        one_lot_currency = tick['averagePositionPrice']['currency']
        current_dynamic_price = tick['expectedYield']['value']
        current_dynamic_currency = tick['expectedYield']['currency']
        current_all_price = (float(balance) * float(one_lot_price) +
                             current_dynamic_price)
        ticker_img = get_ticker_image_link_online(tick['instrumentType'],
                                                  tick['ticker'])

        # Если валюта не рубль, тогда умножаем полную стоимость инструмента
        # на текущую стоимость валюты инструмента
        if one_lot_currency != 'RUB':
            current_all_price = (current_all_price *
                                 price_currency[one_lot_currency])

        # Если нет основного ключа (название вида инструмента), то создаем его
        if instrument_type not in portfolio_dict:
            portfolio_dict.update({instrument_type: {}})
        # Формируем возвращаемый словарь
        portfolio_dict[instrument_type] \
            .update({position_name: {"value": balance,
                                     "total_cost":
                                         round(current_all_price, 2),
                                     "total_cost_currency":
                                         one_lot_currency,
                                     "current_dynamic_price":
                                         round(current_dynamic_price, 2),
                                     "current_dynamic_currency":
                                         current_dynamic_currency,
                                     "ticker_img": ticker_img}})
        # Подсчитываем стоимость портфеля
        portfolio_value += current_all_price
    # Добавляем рубли из портфеля
    portfolio_value += get_portfolio_currency()["RUB"]
    # Обновляем словарь, добавляя в него общую стоимость портфеля
    portfolio_dict.update({"total_portfolio_cost": round(portfolio_value, 2)})

    return portfolio_dict
