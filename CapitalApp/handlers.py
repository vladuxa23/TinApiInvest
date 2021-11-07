import datetime

import CapitalApp
from .models import *
from .rest_wrapper import get_ticker_image_link_online, get_portfolio_currency


# todo: Обработка ошибок разного уровня: транспорта (легли сеть, сервер),
#  превышение лимитов или ошибка в запросе, нужно распарсивать json
# todo: Ежедневная запись в БД
# todo: Веб-приложение/ТГ-бот
# todo: Оптимизация функций
from .utils import DotDict


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


def get_summary() -> dict:
    """
    Функция переформатирует исходный список со словарями (текущее состояние 
    портфеля) в словарь словарей для отображения на странице 
    :param portfolio: список словарей текущего состояния портфеля
    :type portfolio: list 
    :param price_currency: словарь с текущей ценой на валюту в портфеле
    :type price_currency: dict
    :return: dict(instrument_type:dict(name:(dict(instrument_info))))
    """

    portfolio = CapitalApp.rest_wrapper.get_portfolio()

    if portfolio["status"]:
        portfolio = portfolio["resp"]["payload"]["positions"]
        price_currency = {'USD': CapitalApp.rest_wrapper.get_last_price_by_figi(
            'BBG0013HGFT4'),
            'EUR': CapitalApp.rest_wrapper.get_last_price_by_figi(
                'BBG0013HJJ31')}

        # Переменная для подсчёта общей стоимости портфеля
        portfolio_value = 0
        # Словарь, который будет возвращен в результате
        portfolio_dict = dict()

        update_portfolio_data_in_db(portfolio)

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
    else:
        return portfolio


def get_deposits_summary():
    deposits_list = db.session.query(Deposits).all()
    return sum([x.amount for x in deposits_list])


def get_all_credits_info():
    today_ = datetime.date.today()

    credits_list = db.session.query(Credits).all()
    credits_dict = {x.__dict__["name"]: x.__dict__ for x in credits_list}

    for key in credits_dict:
        credits_dict[key].update({"monthly_payment": get_credit_monthly_payment(credits_dict[key]["amount"],
                                                                                credits_dict[key]["percent"],
                                                                                credits_dict[key]["total_month"])})
        credits_dict[key].update({"credit_duration": get_credit_duration(credits_dict[key]["date_start"], today_)})

        remain_info = get_remain_cost(credits_dict[key]["amount"], credits_dict[key]["credit_duration"],
                                      credits_dict[key]["percent"], credits_dict[key]["monthly_payment"])
        credits_dict[key].update({"remain_cost": remain_info["remain_cost"],
                                  "total_body_pay": remain_info["total_body_pay"],
                                  "total_percent_pay": remain_info["total_percent_pay"]})

    return DotDict(credits_dict)

def get_credits_summary():
    credits_list = db.session.query(Credits).all()
    return sum([x.amount for x in credits_list])


def get_credit_monthly_payment(amount, percent, total_month):
    month_percent = percent / (100 * 12)
    return round(amount * (month_percent / (1 - pow((1 + month_percent), -total_month))), 2)


def get_credit_monthly_summary(amount, percent, monthly_payment):
    percent_pay = (percent / 100 / 12) * amount

    return {"body_pay": monthly_payment - percent_pay, "percent_pay": percent_pay}


def get_credit_duration(date_start: datetime.date, today: datetime.date):
    # -1 т.к. в первый месяц оплаты нет
    return abs(today.year - date_start.year) * 12 + today.month - date_start.month - 1


def get_remain_cost(amount, duration, percent, monthly_payment):
    total_body_pay = 0
    total_percent_pay = 0
    for i in range(duration):
        monthly_summary = get_credit_monthly_summary(amount, percent, monthly_payment)
        amount -= monthly_summary["body_pay"]
        total_body_pay += monthly_summary["body_pay"]
        total_percent_pay += monthly_summary["percent_pay"]

    return {"remain_cost": round(amount, 2),
            "total_body_pay": round(total_body_pay, 2),
            "total_percent_pay": round(total_percent_pay, 2)}
