from fastapi import APIRouter, Query
from app.services.currency_service.currency_service import CurrencyService

currency_router = APIRouter()
service = CurrencyService()


@currency_router.get("")
async def get_currency_rates(from_currency: str = Query(..., alias="from"),
                             to_currency: str = Query(..., alias="to"),
                             amount: int = Query(...)):
    result = await service.get_currency_rate(from_currency, to_currency, amount)
    return {"result": result}

