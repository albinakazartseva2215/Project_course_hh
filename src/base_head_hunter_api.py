from abc import abstractmethod, ABC


class BaseHeadHunterAPI(ABC):
    """Базовый абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def connecting_api(self, url, api_key=0):
        """abstractmethod подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self):
        """abstractmethod получения вакансий по ключевому слову"""
        pass