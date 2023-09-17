import datetime

from redis import Redis
from dotenv import load_dotenv
from os import getenv
import json


class CachedDB:

    def __init__(self):
        load_dotenv("app/.env")
        self.__redis = Redis(host=getenv("REDIS_HOST"),
                             port=int(getenv("REDIS_PORT")),
                             decode_responses=True)

    def get_curr_value(self, curr_name: str):
        return self.__redis.get(curr_name)

    def set_curr_value(self, curr_name: str, usd_curr_value: float):
        if curr_name.isupper() and len(curr_name) == 3:
            self.__redis.set(curr_name, usd_curr_value, datetime.timedelta(hours=1))
        else:
            raise AttributeError("Invalid currency name")

    def get_curr_list(self):
        raw = self.__redis.get("list")
        if raw is not None:
            return json.JSONDecoder().decode(raw)
        else:
            return None

    def set_curr_list(self, curr_list: list):
        encoded = json.JSONEncoder().encode(curr_list)
        self.__redis.set("list", encoded, datetime.timedelta(days=1))
