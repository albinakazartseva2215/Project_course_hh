from abc import ABC, abstractmethod


class BaseDBManager(ABC):
    """Базовый абстрактный класс для управления базой данных"""

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """abstractmethod получения список всех компаний и количество вакансий"""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """abstractmethod получения списка всех вакансий"""
        pass

    @abstractmethod
    def get_avg_salary(self):
        """abstractmethod получения средней зарплаты"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """abstractmethod получения вакансий с зарплатой выше средней"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str):
        """abstractmethod получения вакансий по ключевому слову"""
        pass
