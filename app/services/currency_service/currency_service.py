import json
import asyncio
from .url_builder import UrlBuilder
from requests import request
from json import JSONDecoder
from fastapi import HTTPException
from app.db.cached_db import CachedDB
from .request_sender import RequestSender


class CurrencyService:

    def __init__(self):
        self.__url_builder = UrlBuilder()
        self.__cached_db = CachedDB()

    async def get_currency_rate(self, from_curr: str, to_curr: str, amount: int) -> float:
        if self.is_name_valid(from_curr) and self.is_name_valid(to_curr):
            from_value = self.__cached_db.get_curr_value(from_curr)
            to_value = self.__cached_db.get_curr_value(to_curr)
            if (from_value is None) or (to_value is None):
                self.__update_values()
                from_value = self.__cached_db.get_curr_value(from_curr)
                to_value = self.__cached_db.get_curr_value(to_curr)

            return (float(to_value) / float(from_value)) * float(amount)
        else:
            raise HTTPException(status_code=404, detail="No such currency")

    def __update_values(self):
        data = RequestSender.get(url = self.__url_builder.get_live_values())

        if data["success"] is True:
            for i, (curr, rate) in enumerate(data["quotes"].items()):
                self.__cached_db.set_curr_value(curr[3:], float(rate))
            self.__cached_db.set_curr_value("USD", 1)
        else:
            raise HTTPException(status_code=500, detail="Cant update values")

    def __update_list(self):
        data = RequestSender.get(url = self.__url_builder.get_list_values())

        result = [""] * len(data["currencies"])
        if data["success"] is True:
            for i, name in enumerate(data["currencies"]):
                result[i] = name
            self.__cached_db.set_curr_list(result)
        else:
            raise HTTPException(status_code=500, detail="Cant update values")

    def is_name_valid(self, name) -> bool:
        curr_list = self.__cached_db.get_curr_list()
        if curr_list is None:
            self.__update_list()
            curr_list = self.__cached_db.get_curr_list()
        if name in curr_list:
            return True
        else:
            return False


if __name__ == "__main__":
    serv = CurrencyService()
    print(asyncio.run(serv.get_currency_rate("USD", "RUB", 1)))
