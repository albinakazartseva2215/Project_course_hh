import sys

import psycopg2
from psycopg2 import sql


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

    try:
        # Подготовка параметров подключения
        conn_params = {
            "host": params["host"],
            "user": params["user"],
            "password": params["password"],
            "port": params["port"],
            "client_encoding": "utf8",  # Явное указание кодировки
        }

        # Подключение к серверу PostgreSQL
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            # Безопасное создание базы данных
            cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database_name)))

            cur.execute(sql.SQL("CREATE DATABASE {} ENCODING 'UTF8'").format(sql.Identifier(database_name)))

            print(f"База данных {database_name} успешно создана")

        except Exception as e:
            print(f"Ошибка при создании БД: {e}", file=sys.stderr)
            return False
        finally:
            cur.close()
            conn.close()

        # Подключение к новой базе данных
        conn_params["database"] = database_name
        conn = psycopg2.connect(**conn_params)

        try:
            with conn.cursor() as cur:
                # Создание таблиц
                cur.execute(
                    """
                        CREATE TABLE IF NOT EXISTS employers (
                            employer_id INTEGER PRIMARY KEY,
                            employer_name VARCHAR(255) NOT NULL,
                            employer_url VARCHAR(255),
                            description TEXT,
                            open_vacancies INTEGER
                        )
                    """
                )

                cur.execute(
                    """
                        CREATE TABLE IF NOT EXISTS vacancies (
                            vacancy_id SERIAL PRIMARY KEY,
                            employer_id INTEGER REFERENCES employers(employer_id),
                            title VARCHAR(255) NOT NULL,
                            salary_from INTEGER,
                            salary_to INTEGER,
                            experience VARCHAR(255),
                            url VARCHAR(255)
                        )
                    """
                )

            conn.commit()
            print("Таблицы успешно созданы")
            return True

        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}", file=sys.stderr)
            return False
        finally:
            conn.close()

    except Exception as e:
        print(f"Ошибка подключения к PostgreSQL: {e}", file=sys.stderr)
        return False
