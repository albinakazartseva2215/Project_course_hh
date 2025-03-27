import pytest

from src.helper_functions import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, \
    print_vacancies
from src.vacancy import Vacancy


def test_filter_by_name(sample_vacancies):
    """Тест фильтрации по ключевому слову в названии"""
    filter_words = ["python"]
    result = filter_vacancies(sample_vacancies, filter_words)
    assert len(result) == 1
    assert result[0].name == "Python разработчик"


def test_empty_filter_words(sample_vacancies):
    """Тест, что пустой список ключевых слов возвращает все вакансии"""
    filter_words = []
    result = filter_vacancies(sample_vacancies, filter_words)
    assert len(result) == len(sample_vacancies)


def test_no_matches(sample_vacancies):
    """Тест на то, что если нет совпадений, возвращается пустой список"""
    filter_words = ["javascript"]
    result = filter_vacancies(sample_vacancies, filter_words)
    assert len(result) == 0


def test_get_vacancies_by_salary_range_string(sample_vacancies):
    """Тест проверяет, что функция get_vacancies_by_salary() принимает диапазон зарплат в виде строки"""
    result = get_vacancies_by_salary(sample_vacancies, "100000-200000")
    assert len(result) == 3
    salaries = {vac.salary for vac in result}
    assert 100000 in salaries
    assert 150000 in salaries
    assert 200000 in salaries


def test_empty_salary_range(sample_vacancies):
    """Тест проверяет, что при отсутствии диапазона зарплат,
    функция get_vacancies_by_salary() возвращает весь список вакансий """
    result = get_vacancies_by_salary(sample_vacancies, None)
    assert len(result) == len(sample_vacancies)


def test_invalid_salary_range_type():
    """Тест проверяет, что функция get_vacancies_by_salary() корректно обрабатывает
    неправильный тип данных для параметра salary_range"""
    with pytest.raises(ValueError):
        get_vacancies_by_salary([], {"min": 100, "max": 200})


def test_sort_descending(sample_vacancies):
    """Тест на сортировку по убыванию (reverse=True)"""
    sorted_vacancies = sort_vacancies(sample_vacancies, reverse=True)
    salaries = [vac.salary for vac in sorted_vacancies]
    assert salaries == [200000, 150000, 100000, 75000]


def test_sort_ascending(sample_vacancies):
    """Тест на сортировку по возрастанию (reverse=False)"""
    sorted_vacancies = sort_vacancies(sample_vacancies, reverse=False)
    salaries = [vac.salary for vac in sorted_vacancies]
    assert salaries == [75000, 100000, 150000, 200000]


def test_sort_empty_list():
    """Тест на сортировку пустого списка"""
    assert sort_vacancies([]) == []


def test_get_top_exact_number(sample_vacancies):
    """Проверяем получение точного количества вакансий (N равно общему числу)"""
    result = get_top_vacancies(sample_vacancies, 4)
    assert len(result) == 4
    assert result[0].name == "Python разработчик"
    assert result[-1].name == "Backend разработчик"


def test_get_top_zero(sample_vacancies):
    """Проверяем случай с N = 0 (должен вернуть пустой список)"""
    result = get_top_vacancies(sample_vacancies, 0)
    assert len(result) == 0
    assert result == []


def test_get_top_negative_number(sample_vacancies):
    """Проверяем случай с отрицательным N (должен вернуть пустой список)"""
    result = get_top_vacancies(sample_vacancies, -5)
    assert len(result) == 0
    assert result == []


def test_print_single_vacancy(capsys):
    """Тест на вывод одной вакансии"""
    vacancies = [
        Vacancy("Python разработчик", "Mail.ru", "https://hh.ru/vacancy/789", 150000, "5+ лет")
    ]

    print_vacancies(vacancies)

    captured = capsys.readouterr()
    output = captured.out

    assert "Вакансия #1:" in output
    assert "Название: Python разработчик" in output
    assert "Компания: Mail.ru" in output
    assert "Зарплата: 150000." in output
    assert "Ссылка: https://hh.ru/vacancy/789" in output
    assert "Опыт: 5+ лет" in output
    assert "-" * 40 in output
    assert "Вакансия #2" not in output  # Убеждаемся, что только одна вакансия выведена
