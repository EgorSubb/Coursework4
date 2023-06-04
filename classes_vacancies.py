from abc import ABC, abstractmethod
import os
import requests
import json


class ParsingError(Exception):
    """Возвращает текст ошибки при получении данных по API"""

    def __str__(self):
        return 'Ошибка получения данных по API'


class ApiABCClass(ABC):
    """Абстрактный класс для работы с API (HH, SJ)"""

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def formatted_vacancies(self):
        pass


class HeadHunter(ApiABCClass):
    """Класс, который получает список вакансий с Head Hunter и преобразовывает их к общему формату"""

    def __init__(self):
        self.__header = {"User-Agent": "unknown"}
        self.__params = {
            "text": None,
            "page": 0,
            "per_page": 100}
        self.__vacancies = []

    def get_request(self):
        """Запрос по вакансиям Head Hunter"""
        response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['items']

    def get_vacancies(self, keyword, page_count=1):
        """Получает данные по вакансиям с Head Hunter"""
        self.__params["text"] = keyword

        while self.__params['page'] < page_count:

            print(f"HeadHunter, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка при получении данных')
                break
            print(f"Всего {len(values)} вакансий.")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def formatted_vacancies(self):
        """Преобразовывает вакансии к общему формату"""
        formatted_vacancies = []
        for item in self.__vacancies:
            formatted_vacancies.append({
                "source": "HeadHunter",
                "id": int(item["id"]),
                "title": item["name"],
                "client": item["employer"]["name"],
                "link": item["alternate_url"],
                "area": item["area"]["name"]
            })
            if item["salary"] is not None:
                formatted_vacancies[-1]["salary_from"] = item["salary"]["from"]
                formatted_vacancies[-1]["salary_to"] = item["salary"]["to"]
                formatted_vacancies[-1]["salary_currency"] = item["salary"]["currency"]
            else:
                formatted_vacancies[-1]["salary_from"] = formatted_vacancies[-1]["salary_to"] = formatted_vacancies[-1][
                    "salary_currency"] = None
        return formatted_vacancies

    @property
    def vacancies(self):
        return self.__vacancies


class SuperJobAPI(ApiABCClass):
    """Класс, который получает список вакансий с Super Job и преобразовывает их к общему формату"""
    def __init__(self):
        self.__header = {'X-Api-App-Id': os.getenv('SJ_API_KEY')}
        self.__params = {
            "keyword": None,
            "page": 0,
            "count": 100
        }
        self.__vacancies = []

    def get_request(self):
        """Запрос по вакансиям Super Job"""
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['objects']

    def get_vacancies(self, keyword, page_count=1):
        """Получает данные по вакансиям с Super Job"""
        self.__params["keyword"] = keyword

        while self.__params['page'] < page_count:

            print(f"SuperJob, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка при получении данных')
                break
            print(f"Всего {len(values)} вакансий")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def formatted_vacancies(self):
        """Преобразовывает вакансии к общему формату"""
        formatted_vacancies = []
        for item in self.__vacancies:
            formatted_vacancies.append({
                "source": "SuperJob",
                "id": item["id"],
                "title": item["profession"],
                "client": item["firm_name"],
                "link": item["link"],
                "area": item["town"]["title"],
                "salary_from": item["payment_from"],
                "salary_to": item["payment_to"],
                "salary_currency": item["currency"]
            })
            if formatted_vacancies[-1]["salary_from"] == 0:
                formatted_vacancies[-1]["salary_from"] = None
            if formatted_vacancies[-1]["salary_to"] == 0:
                formatted_vacancies[-1]["salary_to"] = None
        return formatted_vacancies
