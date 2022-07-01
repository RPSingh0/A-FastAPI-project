from sqlalchemy import Column, String, DateTime, Float, Integer
from .database import Base


class Trade(Base):
    """
    A class representing the Trade(trading_data) table in the database
    """
    __tablename__ = "trading_data"
    trade_id = Column(String, primary_key=True)
    trader = Column(String)
    trade_date_time = Column(DateTime)
    instrument_id = Column(String)
    instrument_name = Column(String)
    counterparty = Column(String)
    assetClass = Column(String)
    buy_sell_indicator = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
