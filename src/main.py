from src.head_hunter_api import HeadHunterAPI
from src.helper_functions import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, \
    print_vacancies
from src.json_saver import JSONSaver
from src.vacancy import Vacancy

# Пример работы конструктора класса с одной вакансией
vacancy = Vacancy("Data инженер", "Data Inc", 'https://hh.ru/vacancy/456', 120000, 'От 1 года до 3 лет')

# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
json_saver.add_vacancy(vacancy)
json_saver.delete_vacancy(vacancy)

# Функция для взаимодействия с пользователем


def user_interaction() -> None:
    global hh_api
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    if platforms:
        hh_api = HeadHunterAPI()

    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.get_vacancies(search_query)

    # Преобразование набора данных из JSON в список объектов
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    print(user_interaction())
