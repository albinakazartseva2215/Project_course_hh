import sys
import psycopg2
from database import create_database
from head_hunter_api import HeadHunterAPI
from db_manager import DBManager
from config import config
from src.user_interaction import user_interaction


def fill_database(params: dict, employers: list):
    """Заполнение базы данных с обработкой ошибок"""
    global conn
    hh = HeadHunterAPI()
    employers_data = hh.get_employers(employers)

    if not employers_data:
        print("Нет данных о работодателях для добавления")
        return False

    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Вставка работодателей
        for employer in employers_data:
            try:
                cur.execute(
                    """
                    INSERT INTO employers
                    (employer_id, employer_name, employer_url, open_vacancies)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (employer_id) DO NOTHING
                    """,
                    (employer['id'], employer['name'],
                     employer['url'], employer['open_vacancies'])
                )

                # Получаем и вставляем вакансии
                vacancies = hh.get_vacancies(employer['id'])
                if not vacancies:
                    print(f"Нет вакансий для {employer['name']}")
                    continue

                for vacancy in vacancies:
                    try:
                        cur.execute(
                            """
                            INSERT INTO vacancies (
                                vacancy_id, employer_id, title,
                                salary_from, salary_to, experience,
                                url
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (vacancy_id) DO NOTHING
                            """,
                            (
                                vacancy['id'],
                                employer['id'],
                                vacancy['name'],
                                vacancy['salary_from'],
                                vacancy['salary_to'],
                                vacancy['experience'],
                                vacancy['alternate_url']
                            )
                        )
                    except Exception as e:
                        print(f"Ошибка вакансии {vacancy['id']}: {e}")
                        continue

            except Exception as e:
                print(f"Ошибка работодателя {employer['name']}: {e}")
                continue

        conn.commit()
        return True

    except Exception as e:
        print(f"Ошибка БД: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()


def main():
    print(user_interaction())  #по старым методам и функциям
    try:
        # Получаем параметры подключения
        params = config()

        # Создаем базу данных
        if not create_database(params['database'], params):
            raise RuntimeError("Не удалось создать БД")

        # Список компаний
        companies = [
            "Яндекс", "Сбер", "Ozon", "VK", "Верме", "Мегафон",
            "МТС", "Ростелеком", "Tech Horizon", "Газпромнефть"
        ]
        # Заполняем БД
        if not fill_database(params, companies):
            raise RuntimeError("Не удалось заполнить БД")

        # Работа с БД
        db = DBManager(params)

        # Проверка данных
        print("\nПроверка данных в БД:")
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM employers")
                print(f"Работодателей: {cur.fetchone()[0]}")

                cur.execute("SELECT COUNT(*) FROM vacancies")
                print(f"Вакансий: {cur.fetchone()[0]}")

                cur.execute("""
                            SELECT COUNT(*) FROM vacancies
                            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
                        """)
                print(f"Вакансий с зарплатами: {cur.fetchone()[0]}")

        # Вывод результатов
        print("\nКомпании и количество вакансий:")
        for company, count in db.get_companies_and_vacancies_count():
            print(f"- {company}: {count}")

        avg_salary = db.get_avg_salary()
        print(f"\nСредняя зарплата: {avg_salary:.2f} руб." if avg_salary > 0 else "\nНет данных о зарплатах")

        companies_with_high_salary = db.get_vacancies_with_higher_salary()
        print(f"Компании с зарплатой выше среднего: {companies_with_high_salary}")

        keyword = "Python"
        print(f"\nВакансии с ключевым словом '{keyword}':")
        vacancies = db.get_vacancies_with_keyword(keyword)
        if vacancies:
            for i, (company, title, salary_from, salary_to, experience, url) in enumerate(vacancies, 1):
                salary = []
                if salary_from:
                    salary.append(f"от {salary_from}")
                if salary_to:
                    salary.append(f"до {salary_to}")
                salary_str = " ".join(salary) if salary else "не указана"
                if salary and experience:
                    salary_str += f" {experience}"

                print(f"{i}. {company} - {title}")
                print(f"   Зарплата: {salary_str}")
                print(f"   Ссылка: {url}\n")
        else:
            print("Не найдено вакансий с указанными критериями")

    except Exception as e:
        print(f"Критическая ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
