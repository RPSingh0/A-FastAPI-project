from fastapi import HTTPException, status
from .. import models, schemas
from sqlalchemy.orm import Session
from ..models import Trade


def welcome() -> dict:
    """A function that provide basic details about the API"""
    details = {
        "Rupinder Pal Singh": "Hi there, welcome to fast api project",
        "Api endpoints are listed below": {
            "/": "Guide, You are already here!",
            "trade/all": "All the trades sorted by price",
            "trade/id/{id}": "A trade with provided id",
            "trade?search={anything}": "List of trades matching the search parameter",
            "trade/filter?{filter parameters}": "List of trades matching the provided parameters"
        }
    }

    return details


def create_new_trade(request: schemas.Trade, db: Session) -> Trade:
    """A function to create a new record in the database

        Args:
            request [schemas.Trade]: A request representing a record\n
            db [Session]: A database session

        Returns:
            A Trade object if created a record sucessfully

        Exception:
            Raises an exception if any record already exists
    """

    # Check if the trade_id is already available or not
    is_already_available = db.query(models.Trade).filter(
        models.Trade.trade_id.contains(request.trade_id)).first()

    if is_already_available:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"The Trade ID : {request.trade_id} already exists")

    new_trade = models.Trade(trade_id=request.trade_id,
                             trader=request.trader,
                             trade_date_time=request.trade_date_time,
                             instrument_id=request.instrument_id,
                             instrument_name=request.instrument_name,
                             counterparty=request.counterparty,
                             assetClass=request.asset_class,
                             buy_sell_indicator=request.buy_sell_indicator,
                             price=request.price,
                             quantity=request.quantity)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade


def get_all_trades(db: Session) -> list:
    """A function to fetch all the trades in the database

        Args:
            db [Session]: A database session

        Returns:
            A list object representing all the trades in the database sorted by price [low to high]

        Exceptions:
            Raises an exception if database is empty
    """
    trade_query = db.query(models.Trade).order_by(
        models.Trade.price.asc()).all()
    if not trade_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No data available")
    return trade_query


def get_trade_by_id(id: str, db: Session) -> list:
    """A function to fetch a single trade by trade ID

        Args:
            id [str]: A string represenging a trade ID\n
            db [Session]: A database session

        Returns:
            A list object containing a single record

        Exception:
            Raises an exception if trade with the given trade ID is not available
    """
    trade_query = db.query(models.Trade).filter(
        models.Trade.trade_id == id).first()

    if not trade_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trade with id: {id} is not found")

    return trade_query


def search_trades(search: str, db: Session) -> set:
    """A function to fetch all the trades matching the follwing categories:

        counterparty, instrument_id, instrument_name, trader

        Args:
            search [str]: A string containing text to be searched

        Returns:
            A set containing all the trading matching the criteria

        Exceptions:
            Raises an Exception if not trade is found according to specified search
    """
    by_counterparty = db.query(models.Trade).filter(
        models.Trade.counterparty.like(search)).all()

    by_instrument_id = db.query(models.Trade).filter(
        models.Trade.instrument_id.like(search)).all()

    by_instrument_name = db.query(models.Trade).filter(
        models.Trade.instrument_name.like(search)).all()

    by_trader = db.query(models.Trade).filter(
        models.Trade.trader.like(search)).all()

    query_items = []

    # Creating a list containing all the results from all the queries
    for i in [by_counterparty, by_instrument_id, by_instrument_name, by_trader]:
        query_items.extend(i)

    # Removing all the duplicate results for the query_items
    final_query = set(query_items)
    if not final_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found containing : {search}")

    return final_query


def filter_trades(db: Session, **kwargs) -> list:
    """A function to filter and fetch all the trades according to the following parameters if provided:
        assetClass, end, maxPrice(inclusive), minPrice(inclusive), start, tradeType

        **All the parameter are set to `None` by default**

        Args:
            assetClass [str]: asset class of instrument traded\n
            end [dt.datatime]: an object representing the maximum date for trade_date_time field\n
            maxPrice [float]: a float representing the maximum value for price\n
            minPrice [float]: a float representing the minumum value for price\n
            start [dt.datetime]: an object representing the minumum date for trade_date_time field\n
            tradeType [str]: an string representing trade type: [Buy or Sell]\n
            db [Session]: A database session

        Returns:
            a list containing the records filtered by the parameters provided sorted by price[low to high]

        Exception:
            Raises an Exception if no trade is found according to the specifies search
    """
    query_result = db.query(models.Trade)

    if (var := kwargs.get("assetClass")) is not None:
        query_result = query_result.filter(models.Trade.assetClass == var)

    if (var := kwargs.get("end")) is not None:
        query_result = query_result.filter(models.Trade.trade_date_time < var)

    if (var := kwargs.get("start")) is not None:
        query_result = query_result.filter(models.Trade.trade_date_time > var)

    if (var := kwargs.get("maxPrice")) is not None:
        query_result = query_result.filter(models.Trade.price <= var)

    if (var := kwargs.get("minPrice")) is not None:
        query_result = query_result.filter(models.Trade.price >= var)

    if (var := kwargs.get("tradeType")) is not None:
        query_result = query_result.filter(
            models.Trade.buy_sell_indicator == var)

    if not query_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data can be found for applied parameters")

    return query_result.order_by(models.Trade.price.asc()).all()
