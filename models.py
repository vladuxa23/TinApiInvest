from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///capital.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    figi = Column(String(20))
    ticker = Column(String(20))
    isin = Column(String(20))
    instrumentType = Column(String(20))
    balance = Column(Float)
    lots = Column(Integer)
    expectedYieldValue = Column(Float)
    expectedYieldCurrency = Column(String(20))
    averagePositionPriceValue = Column(Float)
    averagePositionPriceCurrency = Column(String(20))
    name = Column(String(200))
    # date = Column(DateTime)

    def __repr__(self):
        return f"<Portfolio(name={self.name}, balance={self.balance}, " \
               f"averagePositionPriceValue={self.averagePositionPriceValue}, averagePositionPriceCurrency={self.averagePositionPriceCurrency})"

