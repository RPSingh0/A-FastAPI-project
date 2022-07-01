from fastapi import FastAPI
from . import models
from .database import engine
from .routers import trade_routers

trading_app = FastAPI()

models.Base.metadata.create_all(engine)

trading_app.include_router(trade_routers.router)
