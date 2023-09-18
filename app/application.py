from fastapi import FastAPI
from.api.api_router import api_router


app = FastAPI(
    title="CurrencyChecker",
    version="0.0.1",
    contact={
        "name": "Roman Kozlov",
        "github": "https://github.com/SoulRiaper",
        "email": "soulriaper@gmail.com"
    },
    description="""
        Try this url http://kozlovrs.ru/api/rates?from=USD&to=RUB&amount=1
    """
)
app.include_router(router=api_router, prefix="/api")

