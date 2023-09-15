from fastapi import APIRouter, Query

currency_router = APIRouter()


@currency_router.get("")
async def get_currency_rates(from_currency: str = Query(..., alias="from"), to_currency: str = Query(..., alias="to")):
    if from_currency == "RUB" and to_currency == "USD":
        return {"IDI": "OTSYUDA"}
    return {"from": from_currency, "to": to_currency}
