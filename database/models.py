# Here is the code for the SQLAlchemy models that represent the tables you requested:

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Equity(Base):
    __tablename__ = "equities"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)

    options = relationship("OptionData", back_populates="equity")


class OptionData(Base):
    __tablename__ = "option_data"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime)
    equity_id = Column(Integer, ForeignKey("equities.id"))
    strike = Column(Float)
    call_or_put = Column(String)
    expiration_date = Column(DateTime)
    last = Column(Float)
    bid = Column(Float)
    ask = Column(Float)
    bid_size = Column(Integer)
    ask_size = Column(Integer)
    open_interest = Column(Integer)
    volume = Column(Integer)
    iv = Column(Float)
    delta = Column(Float)
    gamma = Column(Float)
    vega = Column(Float)
    theta = Column(Float)
    intrinsic_value = Column(Float)

    equity = relationship("Equity", back_populates="options")

