from typing import List, Dict

import requests

from src.base_head_hunter_api import BaseHeadHunterAPI


class HeadHunterAPI(BaseHeadHunterAPI):
    """Класс для подключения к API сайта hh.ru и получения вакансий"""

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 20}
        self.vacancies = []
        super().__init__()


    def connecting_api(self, max_pages: int = 20) -> None:
        """метод подключения к API"""
        while self.params.get('page') < max_pages:
            try:
                response = requests.get(self.url, headers=self.headers, params=self.params, timeout=10)
                if response.status_code == 200:
                    vacancies = response.json()['items']
                    self.vacancies.extend(vacancies)
                    self.params['page'] += 1

                else:
                    raise Exception(f"Ошибка при запросе к API: {response.status_code}, {response.text}")
            except requests.exceptions.Timeout:
                print("Ошибка: Превышено время ожидания ответа от сервера.")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к API: {e}")


    def get_vacancies(self, keyword: str) -> List[Dict]:
        """Метод получения вакансий по ключевому слову"""
        self.params['text'] = keyword
        self.vacancies = []  # Очищаем список вакансий перед новым запросом
        self.connecting_api()
        return self.vacancies


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    try:
        vacancies = hh_api.get_vacancies(keyword="Python")
        print(f"Найдено вакансий: {len(vacancies)}")
        # for vacancy in vacancies[:5]:  # Выводим первые 5 вакансий
        #     print(vacancy['name'], vacancy['alternate_url'])
        print(vacancies[0:1])
    except Exception as e:
        print(e)

