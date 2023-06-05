import json
from classes_vacancies import *
from json_save import JSONSaver


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


def sort_vacancies_from(vacancies: list) -> list:
    """Сортирует вакансии по убыванию минимальной з/п"""
    # Заполняем пустые значения нолями
    for salary in vacancies:
        if salary['salary_from'] is None:
            salary['salary_from'] = 0
    # Сортируем
    sorted_data = sorted(vacancies, key=lambda d: d['salary_from'], reverse=True)
    # Возвращаем пустые значения вместо нолей
    for salary in vacancies:
        if salary['salary_from'] == 0:
            salary['salary_from'] = None
    return sorted_data


def sort_vacancies_to(vacancies: list) -> list:
    """Сортирует вакансии по убыванию максимальной з/п"""
    # Заполняем пустые значения нолями
    for salary in vacancies:
        if salary['salary_to'] is None:
            salary['salary_to'] = 0
    # Сортируем
    sorted_data = sorted(vacancies, key=lambda d: d['salary_to'], reverse=True)
    # Возвращаем пустые значения вместо нолей
    for salary in vacancies:
        if salary['salary_to'] == 0:
            salary['salary_to'] = None
    return sorted_data


def get_top_vacancies(vacancies: list, number) -> list:
    """Возвращает N верхних значений списка вакансий"""
    number = int(number)
    if len(vacancies) > number:
        return vacancies[0:number]
    else:
        return vacancies


def get_vacancies_by_salary(self, salary_min: int, salary_max: int):
    """Возвращает вакансии в диапазоне зарплат"""
    sorted_list = []
    for vacancy in self:
        if isinstance(vacancy["salary_from"], int) and salary_min <= vacancy["salary_from"] <= salary_max:
            sorted_list.append(vacancy)
        elif isinstance(vacancy["salary_to"], int) and salary_min <= vacancy["salary_to"] <= salary_max:
            sorted_list.append(vacancy)
    return sorted_list


def getting_vacancies():
    """Получение вакансий с ресурсов HeadHunter и SuperJob"""

    sources = None
    # Пользователь выбирает ресурс, с которого будут выгружаться данные
    while sources not in ("1", "2", "3"):
        if sources in ("exit", "выход"):
            exit()
        elif sources is not None:
            print('Вы ввели недопустимую команду. Попробуйте снова или введите "exit" для выхода')
        sources = input(
            "Введите требуемые источники вакансий: 1 - HeadHunter, 2 - SuperJob, 3 - HeadHunter + SuperJob\n").lower()

    # Данные будут выгружаться с HeadHunter
    if sources == "1":
        hh = HeadHunter()
        sj = None
    # Данные будут выгружаться с SuperJob
    elif sources == "2":
        hh = None
        sj = SuperJobAPI()
    # Данные будут выгружаться с HeadHunter и с SuperJob
    elif sources == "3":
        hh = HeadHunter()
        sj = SuperJobAPI()

    # Пользователь выбирает ключевое слово, по которому будет осуществляться запрос
    keyword: str = input('Введите требуемое ключевое слово для поиска вакансий\n')

    # Пользователь выбирает с каким количеством страниц будет
    page_count = None
    while page_count not in (range(1, 51)):
        if page_count in ("exit", "выход"):
            exit()
        elif page_count is not None:
            print('Вы ввели недопустимое значение количества страниц.\nПопробуйте снова или введите "exit" для выхода')
        page_count = input(
            "Введите количество страниц вывода, оно не может превышать 50\n")
        if page_count.isdecimal():
            page_count = int(page_count)

    # Получаем данные по вакансиям по ключевому слову и количеству страниц, форматируем внешний вид
    if hh is not None:
        hh.get_vacancies(keyword, int(page_count))
        vacancies_hh = hh.formatted_vacancies()
    else:
        vacancies_hh = []

    if sj is not None:
        sj.get_vacancies(keyword, int(page_count))
        vacancies_sj = sj.formatted_vacancies()
    else:
        vacancies_sj = []

    # Сохраняем данные в JSON файл
    data = JSONSaver(vacancies_hh + vacancies_sj)
    data.save_to_json()
    return data
