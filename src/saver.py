from abc import ABC, abstractmethod


class Saver(ABC):
    @abstractmethod
    def read_data(self):
        """Метод для чтения данных из файла."""
        pass

    @abstractmethod
    def add_vacancy(self, data):
        """Метод для добавления данных в файл."""
        pass

    @abstractmethod
    def delete_vacancy(self, data):
        """Метод для удаления данных из файла."""
        pass