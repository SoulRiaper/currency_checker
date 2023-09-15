from fastapi import APIRouter
from .routes.currency_router import currency_router

api_router = APIRouter()

api_router.include_router(router=currency_router, prefix="/rates")
