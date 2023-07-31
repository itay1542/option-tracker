# Here is the code for the SQLAlchemy models that represent the tables you requested:
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Equity(Base):
    __tablename__ = "equities"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)

    options = relationship("OptionData", back_populates="equity")


class OptionExpirations(Base):
    __tablename__ = "option_expirations"

    datetime = Column(DateTime, primary_key=True, index=True)
    type = Column(String)  # e.g Weekly, Monthly, Quarterly, LEAPS

    options = relationship("OptionData", back_populates="expiration")


class OptionData(Base):
    __tablename__ = "option_data"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime)
    equity_id = Column(Integer, ForeignKey("equities.id"))
    expiration_datetime = Column(Integer, ForeignKey("option_expirations.datetime"))
    strike = Column(Float)
    call_or_put = Column(String)
    type = Column(String)
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
    expiration = relationship("OptionExpirations", back_populates="options")

    @classmethod
    def from_tradestation_api_response(cls, option_dict):
        leg_data = option_dict["Legs"][0]
        return cls(
            datetime=datetime.now(),
            strike=leg_data["StrikePrice"],
            call_or_put=leg_data['OptionType'],
            last=option_dict['Last'],
            bid=option_dict['Bid'],
            ask=option_dict['Ask'],
            type=option_dict['Type'],
            bid_size=option_dict['BidSize'],
            ask_size=option_dict['AskSize'],
            open_interest=option_dict['DailyOpenInterest'],
            volume=option_dict['Volume'],
            iv=option_dict['ImpliedVolatility'],
            delta=option_dict['Delta'],
            gamma=option_dict['Gamma'],
            vega=option_dict['Vega'],
            theta=option_dict['Theta'],
            intrinsic_value=option_dict['IntrinsicValue']
        )
