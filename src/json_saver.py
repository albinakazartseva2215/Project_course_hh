import json
import os
from tabnanny import verbose

from typing import List, Dict, Any, TypeVar

from src.saver import Saver
from src.vacancy import Vacancy

# Создаем TypeVar для типа вакансии
T = TypeVar('T', bound='Vacancy')


class JSONSaver(Saver):
    """Класс для работы с JSON-файлами"""

    def __init__(self, filename: str = "vacancies.json") -> None:
        # Указываем папку data, которая находится на одном уровне с src
        self.__data_folder = os.path.join("..", "data")  # Переход на уровень выше и вход в data
        # Создаем папку data, если она не существует
        if not os.path.exists(self.__data_folder):
            os.makedirs(self.__data_folder)

        # Формируем полный путь к файлу
        self.__filename = os.path.join(self.__data_folder, filename)
        # Создаем файл, если он не существует
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def read_data(self) -> List[Dict[str, Any]]:
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

    def add_vacancy(self, vacancy: T) -> None:
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

    def delete_vacancy(self, data: Dict[str, Any]) -> None:
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
    vacancy_data = Vacancy("Python разработчик", "ПАО МТС", "https://hh.ru/vacancy/123", 100000, "Нет опыта")
    # vacancy_data_dict = vacancy_data.to_dict()
    json_handler.add_vacancy(vacancy_data)

    print(json_handler.read_data())
