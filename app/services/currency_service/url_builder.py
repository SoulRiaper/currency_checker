from dotenv import load_dotenv
from os import getenv


class UrlBuilder:
    def __init__(self):
        load_dotenv(dotenv_path="app/.env")
        self.__api_token = getenv("API_KEY")
        self.__primary_url = f"http://api.currencylayer.com"

    def get_live_values(self) -> str:
        """

        @return: Url for get all currency courses (source USD)
        """
        return f"{self.__primary_url}/live?access_key={self.__api_token}"

    def get_list_values(self) -> str:
        """

        @return: Url for get actual currencies list
        """
        return f"{self.__primary_url}/list?access_key={self.__api_token}"
