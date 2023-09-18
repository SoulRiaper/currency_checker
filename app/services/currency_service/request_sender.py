from requests import request
import json


class RequestSender:

    @staticmethod
    def get(url: str):
        """

        @param url: url for get method
        @return: decoded request result
        """
        res = request("get", url).content.decode("UTF-8")
        return json.JSONDecoder().decode(res)
