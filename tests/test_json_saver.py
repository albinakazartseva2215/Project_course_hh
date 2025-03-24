import json
import os

from src.json_saver import JSONSaver


# Тесты для инициализации
def test_initialization(temp_json_file):
    saver = JSONSaver(filename=temp_json_file)
    assert os.path.exists(temp_json_file)  # Проверяем, что файл создан
    assert saver.read_data() == []  # Проверяем, что файл пуст


# Тесты для метода read_data
def test_read_data_empty_file(json_saver):
    assert json_saver.read_data() == []  # Проверяем чтение пустого файла


def test_read_data_with_content(json_saver):
    test_data = [{"name": "Test Vacancy"}]
    with open(json_saver._JSONSaver__filename, "w", encoding="utf-8") as file:
        json.dump(test_data, file, ensure_ascii=False, indent=4)
    assert json_saver.read_data() == test_data  # Проверяем чтение данных из файла


def test_read_data_invalid_json(json_saver):
    with open(json_saver._JSONSaver__filename, "w", encoding="utf-8") as file:
        file.write("invalid json")
    assert json_saver.read_data() == []  # Проверяем обработку некорректного JSON


# Тесты для метода add_vacancy
def test_add_vacancy(json_saver, sample_vacancy):
    json_saver.add_vacancy(sample_vacancy)
    data = json_saver.read_data()
    assert len(data) == 1  # Проверяем, что вакансия добавлена
    assert data[0] == sample_vacancy.to_dict()  # Проверяем корректность данных


def test_add_vacancy_duplicate(json_saver, sample_vacancy, capsys):
    json_saver.add_vacancy(sample_vacancy)
    json_saver.add_vacancy(sample_vacancy)  # Пытаемся добавить дубликат
    captured = capsys.readouterr()
    assert "Данные уже существуют в файле." in captured.out  # Проверяем сообщение о дубликате
    assert len(json_saver.read_data()) == 1  # Проверяем, что дубликат не добавлен


# Тесты для метода delete_vacancy
def test_delete_vacancy(json_saver, sample_vacancy, capsys):
    json_saver.add_vacancy(sample_vacancy)
    vacancy_dict = sample_vacancy.to_dict()
    json_saver.delete_vacancy(vacancy_dict)
    assert len(json_saver.read_data()) == 0  # Проверяем, что вакансия удалена
