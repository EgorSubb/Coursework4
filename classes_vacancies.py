from abc import ABC, abstractmethod
import os
import requests


class ParsingError(Exception):
    """Возвращает текст ошибки при получении данных по API"""

    def __str__(self):
        return 'Ошибка получения данных по API'


class ComparisonError(Exception):
    """Класс ошибки при сравнении вакансий"""
    def __str__(self):
        return "Ошибка в сравнении.\nВ одной из вакансий не указана з/п"


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

    @property
    def vacancies(self):
        return self.__vacancies

    def get_request(self):
        """Запрос по вакансиям Head Hunter"""
        response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['items']

    def get_vacancies(self, keyword, page_count=1):
        """Получает данные по вакансиям с Head Hunter по ключевому слову"""
        self.__params["text"] = keyword

        while self.__params['page'] < page_count:
            print(f"Cобираем информацию HH со страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка при получении данных')
                break
            print(f"{len(values)} вакансий всего.")
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
                "area": item["area"]["name"]})

            # Отсматриваем исключения, если вилка З/П не указана

            if item["salary"] is not None:
                formatted_vacancies[-1]["salary_from"] = item["salary"]["from"]
                formatted_vacancies[-1]["salary_to"] = item["salary"]["to"]
                formatted_vacancies[-1]["salary_currency"] = item["salary"]["currency"]
            else:
                formatted_vacancies[-1]["salary_from"] = formatted_vacancies[-1]["salary_to"] = formatted_vacancies[-1][
                    "salary_currency"] = None
        return formatted_vacancies


class SuperJobAPI(ApiABCClass):
    """Класс, который получает список вакансий с Super Job и преобразовывает их к общему формату"""
    def __init__(self):
        self.__header = {'X-Api-App-Id': os.getenv('SJ_API_KEY')}
        self.__params = {
            "keyword": None,
            "page": 0,
            "count": 100}

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
        """Получает данные по вакансиям с Super Job по ключевому слову"""
        self.__params["keyword"] = keyword
        print(f"Cобираем информацию SJ со страницы {self.__params['page'] + 1}", end=": ")

        while self.__params['page'] < page_count:
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка при получении данных')
                break
            print(f"{len(values)} вакансий всего")
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
                "salary_currency": item["currency"]})

            # Отсматриваем исключения, если вилка З/П не указана

            if formatted_vacancies[-1]["salary_from"] == 0:
                formatted_vacancies[-1]["salary_from"] = None
            if formatted_vacancies[-1]["salary_to"] == 0:
                formatted_vacancies[-1]["salary_to"] = None
        return formatted_vacancies


class Vacancy:
    """Класс работы с вакансиями"""

    __slots__ = ['source', 'id', 'title', 'employer', 'link', 'area', 'salary_from', 'salary_to', 'salary_currency']
    all_vacancies = []

    def __init__(self, enter_dict: dict):
        """Инициализация класса"""
        self.source = enter_dict['source']
        self.id = enter_dict['id']
        self.title = enter_dict['title']
        self.employer = enter_dict['client']
        self.link = enter_dict['link']
        self.area = enter_dict['area']
        self.salary_from = enter_dict['salary_from']
        self.salary_to = enter_dict['salary_to']
        self.salary_currency = enter_dict['salary_currency']
        self.all_vacancies.append(self)

    def __str__(self):
        """Информация о вакансии для пользователя"""
        return f"""Вакансия {self.title} с ресурса {self.source}"""

    def __repr__(self):
        """Информация о вакансии для разработчика"""
        return f"""Vacancy(source:{self.source}, id:{self.id}, title:{self.title}, employer:{self.employer},
                   link:{self.link}, area:{self.area}, salary_from:{self.salary_from}, salary_to:{self.salary_to},
                   salary_currency:{self.salary_currency}"""

    def __lt__(self, other):
        """Сравнение по з/п"""
        if self.salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.salary_from < other.__salary_from:
                return True
            else:
                return False

    def __le__(self, other):
        """Сравнение по з/п"""
        if self.salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.salary_from <= other.__salary_from:
                return True
            else:
                return False

    def __gt__(self, other):
        """Сравнение по з/п"""
        if self.salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.salary_from > other.__salary_from:
                return True
            else:
                return False

    def __ge__(self, other):
        """Сравнение по з/п"""
        if self.salary_from is None or other.__salary_from is None:
            raise ComparisonError
        else:
            if self.salary_from >= other.__salary_from:
                return True
            else:
                return False
