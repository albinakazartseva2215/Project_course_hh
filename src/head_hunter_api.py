import time
from typing import Dict, List, Optional

import requests

from src.base_api import BaseAPI


class HeadHunterAPI(BaseAPI):
    """Класс для подключения к API сайта hh.ru и получения данных о работодателях и вакансиях"""

    def __init__(self) -> None:
        self.base_url = "https://api.hh.ru"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.timeout = 30  # Увеличиваем таймаут
        super().__init__()

    def _make_request(self, url: str, params: dict = None) -> Optional[dict]:
        """Безопасный запрос с полной обработкой ошибок"""
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)

            # Проверяем статус ответа
            if response.status_code != 200:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return None

            # Парсим JSON только если ответ успешный
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Ошибка соединения: {e}")
            return None
        except ValueError as e:
            print(f"Ошибка парсинга JSON: {e}")
            return None

    def get_employers(self, employer_names: List[str]) -> List[Dict]:
        """Получение данных о работодателях с улучшенной обработкой"""
        employers = []

        for name in employer_names:
            url = f"{self.base_url}/employers"
            params = {"text": name, "only_with_vacancies": True, "per_page": 1}  # Берем только первый результат

            data = self._make_request(url, params)
            if not data or not isinstance(data, dict):
                print(f"Нет данных для работодателя: {name}")
                continue

            items = data.get("items", [])
            if not items:
                print(f"Работодатель не найден: {name}")
                continue

            employer = items[0]
            employers.append(
                {
                    "id": employer.get("id"),
                    "name": employer.get("name"),
                    "url": employer.get("alternate_url"),
                    "open_vacancies": employer.get("open_vacancies", 0),
                }
            )

            time.sleep(0.5)  # Задержка между запросами

        return employers

    def get_vacancies(self, employer_id: int) -> List[Dict]:
        """Получение вакансий с полной проверкой данных"""
        url = f"{self.base_url}/vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": 100,  # Максимальное количество
            "only_with_salary": True,  # Только с указанной зарплатой
        }

        data = self._make_request(url, params)
        if not data or not isinstance(data, dict):
            print(f"Нет данных о вакансиях для работодателя {employer_id}")
            return []

        vacancies = []
        for item in data.get("items", []):
            salary = item.get("salary", {})
            vacancies.append(
                {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "salary_from": salary.get("from"),
                    "salary_to": salary.get("to"),
                    "experience": item["experience"]["name"],
                    "alternate_url": item.get("alternate_url"),
                }
            )

        return vacancies

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """Метод получения вакансий по ключевому слову"""
        url = f"{self.base_url}/vacancies"
        params = {
            "text": keyword,
            "page": 0,
            "per_page": 100,  # Максимальное количество на странице
        }

        try:
            response = self._make_request(url, params)
            if not response or not isinstance(response, dict):
                print(f"API не вернуло данные для ключевого слова: {keyword}")
                return []

            vacancies = []
            for vacancy in response.get("items", []):
                vacancies.append(vacancy)

            return vacancies

        except Exception as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies_with_keyword("нет опыта")
    print(vacancies)
    # try:
    #     vacancies = hh_api.get_vacancies(keyword="Python")
    #     print(f"Найдено вакансий: {len(vacancies)}")
    #     # for vacancy in vacancies[:5]:  # Выводим первые 5 вакансий
    #     #     print(vacancy['name'], vacancy['alternate_url'])
    #     print(vacancies[0:1])
    # except Exception as e:
    #     print(e)
