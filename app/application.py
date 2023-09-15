from fastapi import FastAPI
from.api.api_router import api_router


app = FastAPI()
app.include_router(router=api_router, prefix="/api")

