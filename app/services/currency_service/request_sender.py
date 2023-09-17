from requests import request
import json


class RequestSender:

    @staticmethod
    def get(url: str):
        res = request("get", url).content.decode("UTF-8")
        return json.JSONDecoder().decode(res)
