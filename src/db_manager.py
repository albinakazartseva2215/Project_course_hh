import sys
from typing import List, Tuple

import psycopg2

from src.base_db_manager import BaseDBManager


class DBManager(BaseDBManager):
    """Класс для управления базой данных"""

    def __init__(self, params: dict):
        self.params = params

    def _execute_query(self, query, params=None):
        """Общий метод выполнения запросов"""
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params or ())
                    if cur.description:
                        return cur.fetchall()
                    return None
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}\nЗапрос: {query}", file=sys.stderr)
            raise

    def get_companies_and_vacancies_count(self) -> List[Tuple]:
        """Список компаний и количество вакансий"""
        query = """
            SELECT employer_name, open_vacancies
            FROM employers
            ORDER BY open_vacancies DESC
        """
        return self._execute_query(query)

    def get_all_vacancies(self) -> List[Tuple]:
        """Все вакансии с информацией о компаниях"""
        query = """
            SELECT e.employer_name, v.title,
                   v.salary_from, v.salary_to, v.experience, v.url
            FROM vacancies v
            JOIN employers e USING(employer_id)
        """
        return self._execute_query(query)

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        query = """
            SELECT e.employer_name, v.title,
                   v.salary_from, v.salary_to, v.experience, v.url
            FROM vacancies v
            JOIN employers e USING(employer_id)
            WHERE (COALESCE(v.salary_from, v.salary_to, 0) +
                   COALESCE(v.salary_to, v.salary_from, 0)) / 2 > %s
        """
        return self._execute_query(query, (avg_salary,))

    def get_avg_salary(self) -> float:
        """Расчет средней зарплаты только по вакансиям с данными"""
        query = """
            SELECT AVG((salary_from + salary_to) / 2)
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
        """
        result = self._execute_query(query)
        return round(result[0][0], 2) if result and result[0][0] else 0.0

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает вакансии по ключевому слову"""
        query = """
                SELECT
                    e.employer_name,
                    v.title,
                    v.salary_from,
                    v.salary_to,
                    v.experience,
                    v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.title ILIKE %s
            """
        search_pattern = f"%{keyword}%"
        return self._execute_query(query, (search_pattern,))
