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
        """

        @param from_curr: currency name like "USD" or "EUR"
        @param to_curr: currency name like "USD" or "EUR"
        @param amount: count from currency
        @raise HTTPException : if one of currency names is invalid
        @return: amount of converted currency
        """
        if self.is_name_valid(from_curr) and self.is_name_valid(to_curr):
            from_value = self.__cached_db.get_curr_value(from_curr)
            to_value = self.__cached_db.get_curr_value(to_curr)

            if (from_value is None) or (to_value is None):
                self.__update_values()
                from_value = self.__cached_db.get_curr_value(from_curr)
                to_value = self.__cached_db.get_curr_value(to_curr)

            return (float(to_value) / float(from_value)) * float(amount)
        else:
            raise HTTPException(status_code=404, detail={"error_message": "No such currency"})

    def is_name_valid(self, name) -> bool:
        """
        @param name: currency name
        @return: is currency name is valid
        """
        curr_list = self.__cached_db.get_curr_list()
        if curr_list is None:
            self.__update_list()
            curr_list = self.__cached_db.get_curr_list()
        if name in curr_list:
            return True
        else:
            return False

    def __update_values(self):
        """
        Updates currency rates in database
        @raise HTTPException : if server can`t update currency values
        """
        data = RequestSender.get(url=self.__url_builder.get_live_values())

        if data["success"] is True:
            for i, (curr, rate) in enumerate(data["quotes"].items()):
                self.__cached_db.set_curr_value(curr[3:], float(rate))

            # if USD converts to USD it is 1
            self.__cached_db.set_curr_value("USD", 1)
        else:
            print(f"Error: {data}")
            raise HTTPException(status_code=500, detail={"error_message": "Server error"})

    def __update_list(self):
        """
        Updates list of currencies
        @raise HTTPException : if server can`t update currency list
        """
        data = RequestSender.get(url=self.__url_builder.get_list_values())

        result = [""] * len(data["currencies"])
        if data["success"] is True:
            for i, name in enumerate(data["currencies"]):
                result[i] = name
            self.__cached_db.set_curr_list(result)
        else:
            print(f"Error: {data}")
            raise HTTPException(status_code=500, detail={"error_message": "Server error"})
