# SteelEye API Developer Assignment

### Made with FastAPI, a web framework for building APIs with python

### Following endpoints are provided in the API
* / - Welcome/Guide page
* /trade/all - All the trades sorted by price
* /trade/id/{id}: - A trade with provided id
* trade?search={string} - List of trades matching the search parameter
* trade/filter?{filter parameters} - List of trades matching the provided parameters

### Database used
* Sqlalchemy
  * A dummy database is created and used to test the API
  * Database file: trading_db.db


### File structure

```
    Trading
    |   .gitignore
    |    readme.md
    |    requirement.txt
    |
    |____repository
    |       trade_functions.py
    |
    |____routers
    |       trade_routers.py
    |
    |______init__.py
    |____database.py
    |____main.py
    |____models.py
    |____schemas.py
    |____trading_db.db
```

### A single trade
```
  The trade class contains the following fields:

  * trade_id        * trader             * trade_date_time
  * instrument_id   * instrument_name    * counterparty
  * assetClass      * buy_sell_indicator * price
  * quantity
```

### Trade routes
All the trade routes are handled by trade_routers.py

### Searching
User can request/search data by just providing a search string and API will fetch the data which is based on the search through the following fields:
    
* counterparty
* instrument_id
* instrument_name
* trader

### Filtering data
User can filter the data by providing the following parameters:

* assetClass [str]
* end [datetime.datetime] `yyyy-mm-ddTHH:MM:SS.MS`
* start [datetime.datetime] `yyyy-mm-ddTHH:MM:SS.MS`
* maxPrice [float]
* minPrice [float]
* tradeType [string] `Buy or Sell`

### All the functions and modules in the project are well documented, each and every detail about the parameters, return types and working of functions are provied.


### For working, please refer to the screenshots attached below.