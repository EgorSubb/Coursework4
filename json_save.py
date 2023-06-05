from abc import ABC, abstractmethod
import json


class JsonABC(ABC):
    @abstractmethod
    def save_to_json(self):
        pass

    @abstractmethod
    def delete_vacancy(self, id):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary_min, salary_max):
        pass

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class JSONSaver(JsonABC):

    def __init__(self, data: list):
        self.data = data

    def save_to_json(self):
        """Сохраняет данные в файл в формате json"""
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file)

    def delete_vacancy(self, vacancy_id: int):
        """Удаляет вакансию из файла"""
        file = open('data.json', 'r', encoding='utf-8')
        data = json.load(file)
        file.close()
        del_dict = None
        for i in range(len(data)):
            if data[i]["id"] == vacancy_id:
                del_dict = data[i]
        if del_dict is None:
            print("В списке вакансий нет вакансии с таким id")
        else:
            data.remove(del_dict)
        self.data = data
        file = open('data.json', 'w', encoding='utf-8')
        json.dump(data, file)
        file.close()

    def get_vacancies_by_salary(self, salary_min: int, salary_max: int):
        """Получает данные по вакансиям по вилке зарплаты"""
        answer = []
        for vacancy in self.data:
            if isinstance(vacancy["salary_from"], int) and salary_min <= vacancy["salary_from"] <= salary_max:
                answer.append(vacancy)
            elif isinstance(vacancy["salary_to"], int) and salary_min <= vacancy["salary_to"] <= salary_max:
                answer.append(vacancy)
        return answer
