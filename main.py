from json_save import *
from utils import *


def main():

    # Получаем данные с нужных сайтов

    data = getting_vacancies()
    vacancies_all = data.data

    while True:

        # Вывод пользовательского меню
        print(f'В полученном списке {len(vacancies_all)} вакансий')
        print("""Введите одну из предложенных команд:
              '1 - Показать N верхних вакансий из списка'
              '2 - Отсортировать вакансии по убыванию максимальной зарплаты'
              '3 - Отсортировать вакансии по убыванию минимальной зарплаты'
              '4 - Отфильтровать вакансии в диапазоне зарплат'
              '5 - Удалить вакансию из общего файла по id'
              '"print" - Вывести вакансии в консоль'
              '"exit" - выход'""")

        # Ввод команды пользователем
        user_input = input().lower()

        # Активация функций в зависимости от ввода пользователя

        # Показать количество верхних вакансий из списка
        if user_input == "1":
            number = input('Введите количество верхних вакансий из списка ')
            if number.isdecimal():
                vacancies_all = get_top_vacancies(vacancies_all, number)
            else:
                print('Некорректное значение')

        # Показать вакансии по убыванию максимальной зарплаты
        elif user_input == "2":
            vacancies_all = sort_vacancies_to(vacancies_all)

        # Показать вакансии по убыванию минимальной зарплаты
        elif user_input == "3":
            vacancies_all = sort_vacancies_from(vacancies_all)

        # Показать вакансии в диапазоне зарплат "от и до"
        elif user_input == "4":
            salaries = input('Введите минимальное и максимальное значение зарплат через пробел\n').strip()
            if salaries.split()[0].isdecimal():
                salary_min = int(salaries.split()[0])
            else:
                print('Некорректное значение')
                salary_min = None
            if salaries.split()[1].isdecimal():
                salary_max = int(salaries.split()[0])
            else:
                print('Некорректное значение')
                salary_max = None
            if salary_max is not None and salary_min is not None:
                vacancies_all = get_vacancies_by_salary(vacancies_all, salary_min, salary_max)

        # Удалить вакансию из общего файла по id
        elif user_input == "5":
            vacancy_id = input('Введите id вакансии, которую хотите удалить\n')
            if vacancy_id.isdecimal():
                vacancy_id = int(vacancy_id)
                data.delete_vacancy(vacancy_id)
                vacancies_all = data.data
            else:
                print('Некорректное значение')

        # Вывести вакансии в консоль
        elif user_input == "print":
            printj(vacancies_all)

        # Выйти
        elif user_input == "exit":
            exit()
        else:
            print('Введена некорректная команда.\nПопробуйте снова или введите "exit" для выхода')


if __name__ == '__main__':
    main()
