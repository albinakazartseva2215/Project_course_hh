def filter_vacancies(vacancies_list: list, filter_words: str) -> list:
    """
    Фильтрует список вакансий по ключевым словам.
    :param vacancies_list: Список объектов Vacancy.
    :param filter_words: Список ключевых слов для фильтрации.
    :return: Отфильтрованный список объектов Vacancy.
    """
    if not filter_words:
        return vacancies_list  # Если ключевые слова не указаны, возвращаем весь список

    filtered_vacancies = []
    for vacancy in vacancies_list:
        # Проверяем, содержатся ли ключевые слова в названии вакансии, компании или опыте
        for word in filter_words:
            if (word.lower() in vacancy.name.lower() or
                    word.lower() in vacancy.company.lower() or
                    word.lower() in vacancy.experience.lower()):
                filtered_vacancies.append(vacancy)
                break  # Если хотя бы одно слово найдено, добавляем вакансию и выходим из цикла
    return filtered_vacancies

def get_vacancies_by_salary(filtered_vacancies, salary_range):
    """
    Фильтрует список вакансий по диапазону зарплат.
    :param filtered_vacancies: Список объектов Vacancy.
    :param salary_range: Диапазон зарплат в формате "min-max" или [min, max].
    :return: Отфильтрованный список объектов Vacancy.
    """
    if not salary_range:
        return filtered_vacancies  # Если диапазон не указан, возвращаем весь список

    # Преобразуем salary_range в список [min, max]
    if isinstance(salary_range, str):
        try:
            min_salary, max_salary = map(int, salary_range.split("-"))
        except ValueError:
            raise ValueError("Диапазон зарплат должен быть в формате 'min-max'.")
    elif isinstance(salary_range, (list, tuple)) and len(salary_range) == 2:
        min_salary, max_salary = salary_range
    else:
        raise ValueError("Диапазон зарплат должен быть строкой 'min-max' или списком [min, max].")

    # Фильтруем вакансии по диапазону зарплат
    filtered_by_salary = []
    for vacancy in filtered_vacancies:
        if min_salary <= vacancy.salary <= max_salary:
            filtered_by_salary.append(vacancy)

    return filtered_by_salary

def sort_vacancies(vacancies, reverse=True):
    """
    Сортирует список вакансий по зарплате.
    :param vacancies: Список объектов Vacancy.
    :param reverse: Если True, сортировка по убыванию зарплаты.
    :return: Отсортированный список объектов Vacancy.
    """
    return sorted(vacancies, key=lambda x: x.salary, reverse=reverse)


def get_top_vacancies(vacancies, top_n):
    """
    Возвращает топ-N вакансий из списка.
    :param vacancies: Список объектов Vacancy.
    :param top_n: Количество вакансий для возврата.
    :return: Список из топ-N объектов Vacancy.
    """
    if top_n <= 0:
        return []  # Если top_n не положительное число, возвращаем пустой список
    return vacancies[:top_n]


def print_vacancies(vacancies):
    """
    Выводит информацию о вакансиях в удобочитаемом формате.
    :param vacancies: Список объектов Vacancy.
    """
    if not vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    for index, vacancy in enumerate(vacancies, start=1):
        print(f"Вакансия #{index}:")
        print(f"Название: {vacancy.name}")
        print(f"Компания: {vacancy.company}")
        print(f"Зарплата: {vacancy.salary}.")
        print(f"Ссылка: {vacancy.alternate_url}")
        print(f"Опыт: {vacancy.experience}")
        print("-" * 40)  # Разделитель между вакансиями
