from datetime import datetime

from CapitalApp import db


class Portfolio(db.Model):
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    lots = db.Column(db.Integer)
    expected_yield_value = db.Column(db.Float)
    average_position_price_value = db.Column(db.Float)

    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument_info.id'))
    expected_yield_currency_id = db.Column(db.Integer, db.ForeignKey("currency.id"))
    average_position_price_currency_id = db.Column(db.Integer, db.ForeignKey("currency.id"))

    # instrument = db.relationship('InstrumentInfo', backref=db.backref('1', lazy=True))
    # expected_yield_currency = db.relationship('Currency', backref=db.backref('2', lazy=True))
    # average_position_price_currency = db.relationship('Currency', backref=db.backref('3', lazy=True))

    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Portfolio<averagePositionPriceValue={self.averagePositionPriceValue}, " \
               f"averagePositionPriceCurrency={self.averagePositionPriceCurrency})>"


class Currency(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), unique=True)

    def __repr__(self):
        return f"Currency<({self.currency})>"


class InstrumentInfo(db.Model):
    __tablename__ = "instrument_info"
    id = db.Column(db.Integer, primary_key=True)
    figi = db.Column(db.String(20), unique=True)
    ticker = db.Column(db.String(20), unique=True)
    isin = db.Column(db.String(20))
    instrument_type = db.Column(db.String(20))
    name = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return f"InstrumentInfo<name={self.name}, balance={self.balance}>"


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

    def __repr__(self):
        return f"Ticker {self.ticker} image {self.imagelink}"
