
from fastapi import APIRouter, Depends
from ..database import get_database
from sqlalchemy.orm import Session
from ..repository import trade_functions
from .. import schemas
from typing import Optional
import datetime as dt
from ..models import Trade

router = APIRouter(tags=["Trading"])


@router.get("/")
def welcome() -> dict:
    return trade_functions.welcome()


@router.post("/trade/create")
def new_trade(request: schemas.Trade, db: Session = Depends(get_database)) -> Trade:
    return trade_functions.create_new_trade(request, db)


@router.get("/trade/all")
def get_all_trades(db: Session = Depends(get_database)) -> list:
    return trade_functions.get_all_trades(db)


@router.get("/trade/id/{id}")
def get_trade_by_id(id: str, db: Session = Depends(get_database)) -> list:
    return trade_functions.get_trade_by_id(id, db)


@router.get("/trade")
def search_trades(search: str, db: Session = Depends(get_database)) -> set:
    return trade_functions.search_trades(search, db)


@router.get("/trade/filter")
def filter_trades(assetClass: Optional[str] = None, end: Optional[dt.datetime] = None,
                  maxPrice: Optional[float] = None, minPrice: Optional[float] = None,
                  start: Optional[dt.datetime] = None, tradeType: Optional[str] = None,
                  db: Session = Depends(get_database)) -> list:

    return trade_functions.filter_trades(db,
                                         assetClass=assetClass,
                                         end=end,
                                         maxPrice=maxPrice,
                                         minPrice=minPrice,
                                         start=start,
                                         tradeType=tradeType)
