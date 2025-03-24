import pytest

from src.vacancy import Vacancy


# Тесты для инициализации и валидации
def test_vacancy_initialization(sample_vacancy):
    assert sample_vacancy.name == "Python разработчик"
    assert sample_vacancy.company == "ПАО МТС"
    assert sample_vacancy.alternate_url == "https://hh.ru/vacancy/123"
    assert sample_vacancy.salary == 100000
    assert sample_vacancy.experience == "1-3 года"


def test_validate_name():
    with pytest.raises(ValueError, match="Название вакансии должно быть непустой строкой."):
        Vacancy(
            name="", company="ПАО МТС", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
        )


def test_validate_company():
    with pytest.raises(ValueError, match="Название компании должно быть непустой строкой."):
        Vacancy(
            name="Python разработчик",
            company="",
            alternate_url="https://hh.ru/vacancy/123",
            salary=100000,
            experience="1-3 года",
        )


def test_validate_salary():
    with pytest.raises(ValueError, match="Зарплата должна быть положительным числом."):
        Vacancy(
            name="Python разработчик",
            company="ПАО МТС",
            alternate_url="https://hh.ru/vacancy/123",
            salary=-1000,
            experience="1-3 года",
        )


def test_validate_alternate_url():
    with pytest.raises(ValueError, match="Ссылка на вакансию должна быть строкой и начинаться с http."):
        Vacancy(
            name="Python разработчик",
            company="ПАО МТС",
            alternate_url="invalid_url",
            salary=100000,
            experience="1-3 года",
        )


def test_validate_experience():
    with pytest.raises(ValueError, match="Название компании должно быть непустой строкой."):
        Vacancy(
            name="Python разработчик",
            company="ПАО МТС",
            alternate_url="https://hh.ru/vacancy/123",
            salary=100000,
            experience="",
        )


# Тесты для магических методов сравнения
def test_eq(sample_vacancy):
    vacancy1 = Vacancy(
        name="A", company="B", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
    )
    vacancy2 = Vacancy(
        name="C", company="D", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
    )
    assert vacancy1 == vacancy2


def test_lt(sample_vacancy):
    vacancy1 = Vacancy(
        name="A", company="B", alternate_url="https://hh.ru/vacancy/123", salary=50000, experience="1-3 года"
    )
    vacancy2 = Vacancy(
        name="C", company="D", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
    )
    assert vacancy1 < vacancy2


def test_le(sample_vacancy):
    vacancy1 = Vacancy(
        name="A", company="B", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
    )
    vacancy2 = Vacancy(
        name="C", company="D", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
    )
    assert vacancy1 <= vacancy2


def test_gt(sample_vacancy):
    vacancy1 = Vacancy(
        name="A", company="B", alternate_url="https://hh.ru/vacancy/123", salary=150000, experience="1-3 года"
    )
    vacancy2 = Vacancy(
        name="C", company="D", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
    )
    assert vacancy1 > vacancy2


def test_ge(sample_vacancy):
    vacancy1 = Vacancy(
        name="A", company="B", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
    )
    vacancy2 = Vacancy(
        name="C", company="D", alternate_url="https://hh.ru/vacancy/123", salary=100000, experience="1-3 года"
    )
    assert vacancy1 >= vacancy2


# Тесты для методов to_dict и from_dict
def test_to_dict(sample_vacancy):
    expected_dict = {
        "вакансия": "Python разработчик",
        "компания": "ПАО МТС",
        "url": "https://hh.ru/vacancy/123",
        "зарплата": 100000,
        "опыт": "1-3 года",
    }
    assert sample_vacancy.to_dict() == expected_dict


def test_from_dict():
    data = {
        "вакансия": "Python разработчик",
        "компания": "ПАО МТС",
        "url": "https://hh.ru/vacancy/123",
        "зарплата": 100000,
        "опыт": "1-3 года",
    }
    vacancy = Vacancy.from_dict(data)
    assert vacancy.name == "Python разработчик"
    assert vacancy.company == "ПАО МТС"
    assert vacancy.alternate_url == "https://hh.ru/vacancy/123"
    assert vacancy.salary == 100000
    assert vacancy.experience == "1-3 года"


# Тесты для метода cast_to_object_list
def test_cast_to_object_list():
    data = [
        {
            "name": "Python разработчик",
            "employer": {"name": "ПАО МТС"},
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 90000, "to": 110000},
            "experience": {"name": "1-3 года"},
        },
        {
            "name": "Data инженер",
            "employer": {"name": "Data Inc"},
            "alternate_url": "https://hh.ru/vacancy/125",
            "salary": {"from": 120000, "to": None},
            "experience": {"name": "3-5 лет"},
        },
    ]
    vacancies = Vacancy.cast_to_object_list(data)
    assert len(vacancies) == 2
    assert vacancies[0].name == "Python разработчик"
    assert vacancies[0].salary == 100000  # Среднее значение (90000 + 110000) // 2
    assert vacancies[1].name == "Data инженер"
    assert vacancies[1].salary == 120000  # Используется salary_from, так как salary_to отсутствует


# Тесты для строкового представления
def test_str(sample_vacancy):
    expected_str = (
        "Вакансия: Python разработчик в компании ПАО МТС "
        "с опытом '1-3 года' и зарплатой 100000 руб. "
        "Ссылка: https://hh.ru/vacancy/123"
    )
    assert str(sample_vacancy) == expected_str


def test_repr(sample_vacancy):
    expected_repr = (
        "Vacancy(name='Python разработчик', company='ПАО МТС', "
        "alternate_url='https://hh.ru/vacancy/123', salary=100000, "
        "experience='1-3 года')"
    )
    assert repr(sample_vacancy) == expected_repr
