import pytest


def test_initialization(hh_api):
    """Тест проверяет корректность инициализации объекта класса."""
    assert hh_api.url == "https://api.hh.ru/vacancies"
    assert hh_api.headers == {"User-Agent": "HH-User-Agent"}
    assert hh_api.params == {"text": "", "page": 0, "per_page": 20}
    assert hh_api.vacancies == []


def test_connecting_api(hh_api, requests_mock):
    """Тест проверяет корректность работы метода connecting_api при успешном ответе от API."""
    mock_url = "https://api.hh.ru/vacancies"
    mock_response = {"items": [{"id": "1", "name": "Python разработчик"}]}
    requests_mock.get(mock_url, json=mock_response, status_code=200)

    hh_api.connecting_api(max_pages=1)
    assert len(hh_api.vacancies) == 1
    assert hh_api.vacancies[0]["id"] == "1"
    assert hh_api.vacancies[0]["name"] == "Python разработчик"


def test_get_vacancies(hh_api, requests_mock):
    """Тест проверяет корректность работы метода get_vacancies при успешном ответе от API."""
    mock_url = "https://api.hh.ru/vacancies"
    mock_response = {"items": [{"id": "2", "name": "Data инженер"}]}
    requests_mock.get(mock_url, json=mock_response, status_code=200)

    vacancies = hh_api.get_vacancies(keyword="Data инженер", max_pages=1)
    assert len(vacancies) == 1
    assert vacancies[0]["id"] == "2"
    assert vacancies[0]["name"] == "Data инженер"


def test_connecting_api_error_response(hh_api, requests_mock):
    """Тест проверяет обработку ошибки HTTP-запроса (например, код 400)."""
    mock_url = "https://api.hh.ru/vacancies"
    requests_mock.get(mock_url, status_code=400, text="Bad Request")

    with pytest.raises(Exception) as exc_info:
        hh_api.connecting_api(max_pages=1)
    assert "Ошибка при запросе к API: 400" in str(exc_info.value)
