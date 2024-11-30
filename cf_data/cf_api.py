import requests

from settings import BASE_URL


class APIClient:
    @staticmethod
    def get():
        """
        Функция возвращает список словарей, содержащих данные о задачах.
        :return:
        """

        response = requests.get(BASE_URL)
        response.raise_for_status()

        return response.json()['result']
