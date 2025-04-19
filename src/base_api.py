from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Базовый абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str):
        """abstractmethod получения вакансий по ключевому слову"""
        pass
