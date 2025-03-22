import json
import os
from tabnanny import verbose
from typing import TextIO

from src.saver import Saver
from src.vacancy import Vacancy


class JSONSaver(Saver):
    """Класс для работы с JSON-файлами"""

    def __init__(self, filename="vacancies.json"):
        self.__filename = filename
        # Создаем файл, если он не существует
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def read_data(self):
        """Метод для чтения данных из JSON-файла."""
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                # Проверяем, не пуст ли файл
                if os.path.getsize(self.__filename) == 0:
                    return []
                return json.load(file)
        except json.JSONDecodeError:
            # Если файл содержит некорректный JSON, возвращаем пустой список
            return []

    def add_vacancy(self, vacancy):
        """Метод для добавления данных в JSON-файл без дублирования."""
        existing_data = self.read_data()
        vacancy_dict = vacancy.to_dict()
        # Проверяем, есть ли данные уже в файле
        if vacancy_dict not in existing_data:
            existing_data.append(vacancy_dict)
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)
        else:
            print("Данные уже существуют в файле.")

    def delete_vacancy(self, data):
        """Удаление данных из JSON-файла."""
        existing_data = self.read_data()
        if data in existing_data:
            existing_data.remove(data)
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)
        elif verbose:
            print("Данные не найдены в файле.")


if __name__ == "__main__":
    json_handler = JSONSaver()
    vacancy_data = Vacancy("Python разработчик", "ПАО МТС", 'https://hh.ru/vacancy/123', 100000, 'Нет опыта')
    vacancy_data_dict = vacancy_data.to_dict()
    json_handler.add_vacancy(vacancy_data_dict)

    print(json_handler.read_data())

    json_handler.delete_data(vacancy_data)