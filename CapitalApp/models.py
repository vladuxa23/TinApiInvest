import datetime

from CapitalApp import db


def get_currency_id(currency_dict: dict) -> int:
    """
    Функция возвращает id валюты в БД, получая данные из словаря

    :param currency_dict: словарь содержащий информацио о валюте портфеля
    :type currency_dict: dict

    :rtype: int
    :return: int currency id in database
    """

    # Если нет данных о валюте в бд
    if Currency.query.filter_by(currency=currency_dict['currency'])\
            .first() is None:
        # то добавляем их
        db.session.add(Currency(currency_dict['currency']))
        db.session.commit()
    # И возвращаем id
    return Currency.query.filter_by(currency=currency_dict['currency'])\
        .first().id


def get_instrument_type_id(instrument_dict):
    if InstrumentInfo.query.filter_by(ticker=instrument_dict.get('ticker'))\
            .first() is None:
        # Если не существует, добавляем его
        db.session.add(InstrumentInfo(**instrument_dict))
        # Сохраняем состояние БД
        db.session.commit()
        # Возвращаем кортеж со временем добавления
    return InstrumentInfo.query.filter_by(ticker=instrument_dict.get('ticker'))\
        .first().id


class Portfolio(db.Model):
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    lots = db.Column(db.Integer)
    expected_yield_value = db.Column(db.Float)
    average_position_price_value = db.Column(db.Float)

    instrument_id = db.Column(db.Integer,
                              db.ForeignKey('instrument_info.id'))
    expected_yield_currency_id = db.Column(db.Integer,
                                           db.ForeignKey("currency.id"))
    average_position_price_currency_id = db.Column(db.Integer,
                                                   db.ForeignKey("currency.id"))

    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<instrument_id={self.id}"

    def __init__(self, **kwargs):
        self.balance = kwargs.get('balance')
        self.lots = kwargs.get('lots')
        self.expected_yield_value = kwargs.get('expectedYield').get('value')
        self.average_position_price_value = kwargs.get('averagePositionPrice')\
            .get('value')
        self.instrument_id = get_instrument_type_id(kwargs)
        self.expected_yield_currency_id = get_currency_id(kwargs
                                                          .get('expectedYield'))
        self.average_position_price_currency_id = \
            get_currency_id(kwargs.get('averagePositionPrice'))


class Currency(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), unique=True)

    def __init__(self, currency):
        self.currency = currency


class InstrumentInfo(db.Model):
    __tablename__ = "instrument_info"
    id = db.Column(db.Integer, primary_key=True)
    figi = db.Column(db.String(20), unique=True)
    ticker = db.Column(db.String(20), unique=True)
    isin = db.Column(db.String(20))
    instrument_type = db.Column(db.String(20))
    name = db.Column(db.String(200), unique=True)

    def __init__(self, **kwargs):
        self.figi = kwargs.get('figi')
        self.ticker = kwargs.get('ticker')
        self.isin = kwargs.get('isin')
        self.instrument_type = kwargs.get('instrumentType')
        self.name = kwargs.get('name')


class TickerImage(db.Model):
    __tablename__ = "ticker_image"
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String)
    imagelink = db.Column(db.String(255))
    image = db.Column(db.BLOB)

    def __init__(self, ticker: str, imagelink: str, image):
        self.ticker = ticker
        self.imagelink = imagelink
        self.image = image


class Credits(db.Model):
    __tablename__ = 'credits'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_start = db.Column(db.Date)
    total_month = db.Column(db.Integer)
    percent = db.Column(db.Float)
    amount = db.Column(db.Float)
    amount_value = db.Column(db.Integer, db.ForeignKey("currency.id"))

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.date_start = datetime.datetime.strptime(kwargs.get('date_start'),
                                            '%d.%m.%Y')
        self.total_month = int(kwargs.get('total_month'))
        self.percent = float(kwargs.get('percent'))
        self.amount = float(kwargs.get('amount'))
        self.amount_value = kwargs.get('amount_value')


class Deposits(db.Model):
    __tablename__ = 'deposits'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_start = db.Column(db.Date)
    percent = db.Column(db.Float)
    amount = db.Column(db.Float)
    amount_value = db.Column(db.Integer, db.ForeignKey("currency.id"))

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.date_start = datetime.datetime.strptime(kwargs.get('date_start'),
                                            '%d.%m.%Y')
        self.percent = float(kwargs.get('percent'))
        self.amount = float(kwargs.get('amount'))
        self.amount_value = kwargs.get('amount_value')

