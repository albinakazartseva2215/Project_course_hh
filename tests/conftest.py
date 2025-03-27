import json
import os
import tempfile

import pytest

from src.head_hunter_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


@pytest.fixture
def sample_vacancy():
    return Vacancy(
        name="Python разработчик",
        company="ПАО МТС",
        alternate_url="https://hh.ru/vacancy/123",
        salary=100000,
        experience="1-3 года",
    )


@pytest.fixture
def temp_json_file():
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", suffix=".json", encoding="utf-8") as temp_file:
        temp_file.write(json.dumps([]))  # Создаем пустой JSON-файл
        temp_file_path = temp_file.name
    yield temp_file_path  # Возвращаем путь к временному файлу
    os.remove(temp_file_path)  # Удаляем временный файл после завершения теста


# Фикстура для создания объекта JSONSaver с временным файлом
@pytest.fixture
def json_saver(temp_json_file):
    return JSONSaver(filename=temp_json_file)


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python разработчик", "Yandex", "https://hh.ru/vacancy/125", 100000, "1-3 года"),
        Vacancy("Java разработчик", "Google", "https://hh.ru/vacancy/138", 150000, "3-5 лет"),
        Vacancy("Data инженер", "Yandex", "https://hh.ru/vacancy/166", 75000, "no experience"),
        Vacancy("Backend разработчик", "Mail.ru", "https://hh.ru/vacancy/333", 200000, "5+ years"),
    ]
