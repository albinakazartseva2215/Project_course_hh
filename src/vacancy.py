class Vacancy():
    __slots__ = ['name', 'company', 'alternate_url', 'salary', 'experience']

    def __init__(self, name, company, alternate_url, salary, experience):
        self.name = self._validate_name(name)
        self.company = self._validate_company(company)
        self.alternate_url = self._validate_alternate_url(alternate_url)
        self.salary = self._validate_salary(salary)
        self.experience = self._validate_experiance(experience)

    def _validate_name(self, name: str) -> str:
        """Метод проверяет, что название вакансии является непустой строкой."""

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название вакансии должно быть непустой строкой.")
        return name

    def _validate_company(self, company: str) -> str:
        """Метод проверяет, что название компании является непустой строкой."""
        if not isinstance(company, str) or not company.strip():
            raise ValueError("Название компании должно быть непустой строкой.")
        return company

    def _validate_salary(self, salary: int | float) -> int | float:
        """Метод проверяет, что зарплата является положительным числом."""
        if not isinstance(salary, (int, float)) or salary < 0:
            raise ValueError("Зарплата должна быть положительным числом.")
        return salary

    def _validate_alternate_url(self, alternate_url: str) -> str:
        """Метод проверяет, что ссылка на вакансию является валидным URL."""
        if not isinstance(alternate_url, str) or not alternate_url.startswith("http"):
            raise ValueError("Ссылка на вакансию должна быть строкой и начинаться с http.")
        return alternate_url


    def _validate_experiance(self, experience) -> str:
        """Метод проверяет, что опыт работы является непустой строкой."""
        if not isinstance(experience, str) or not experience.strip():
            raise ValueError("Название компании должно быть непустой строкой.")
        return experience

    def __eq__(self, other):
        """Магический метод проверяет равенство зарплат двух вакансий."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary

    def __lt__(self, other):
        """Магический метод проверяет, меньше ли зарплата текущей вакансии, чем у другой."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __le__(self, other):
        """Магический метод проверяет, меньше или равна ли зарплата текущей вакансии, чем у другой."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary <= other.salary

    def __gt__(self, other):
        """Магический метод проверяет, больше ли зарплата текущей вакансии, чем у другой."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary

    def __ge__(self, other):
        """Магический метод проверяет, больше или равна ли зарплата текущей вакансии, чем у другой."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary >= other.salary

    def __repr__(self):
        """Магический метод для отображения информации об объекте класса в режиме отладки"""
        return f"Vacancy(name={self.name!r}, company={self.company!r}, alternate_url={self.alternate_url!r}, salary={self.salary!r}, experience={self.experience!r})"

    def __str__(self) -> str:
        """Магический метод для отображения информации об объекте класса для пользователей"""
        return f"Вакансия: {self.name} в компании {self.company} с опытом '{self.experience}' и зарплатой {self.salary} руб. Ссылка: {self.alternate_url}"


    def to_dict(self) -> dict:
        """
        Преобразует объект Vacancy в словарь.
        :return: Словарь с атрибутами объекта.
        """
        return {
            "вакансия": self.name,
            "компания": self.company,
            "url": self.alternate_url,
            "зарплата": self.salary,
            "опыт": self.experience
        }

    @classmethod
    def from_dict(cls, data):
        """Создает объект Vacancy из словаря."""
        return cls(
            name=data.get("вакансия"),
            company=data.get("компания"),
            alternate_url=data.get("url"),
            salary=data.get("зарплата"),
            experience=data.get("опыт")
        )

    @staticmethod
    def cast_to_object_list(data):
        """
        Преобразует JSON-данные (список словарей) в список объектов Vacancy.
        :param data: Список словарей с данными о вакансиях.
        :return: Список объектов Vacancy.
        """
        vacancies = []
        for item in data:
            # Обработка зарплаты
            salary_info = item.get("salary")
            if salary_info:
                salary_from = salary_info.get("from")
                salary_to = salary_info.get("to")
                # Используем среднее значение, если указаны оба значения
                if salary_from is not None and salary_to is not None:
                    salary = (salary_from + salary_to) // 2
                elif salary_from is not None:
                    salary = salary_from
                elif salary_to is not None:
                    salary = salary_to
                else:
                    salary = 0  # Если зарплата не указана
            else:
                salary = 0  # Если ключ "salary" отсутствует

            # Создаем объект Vacancy
            vacancy = Vacancy(
                name=item.get("name"),
                company=item.get("employer", {}).get("name"),
                alternate_url=item.get("alternate_url"),
                salary=salary,
                experience=item.get("experience", {}).get("name")
            )
            vacancies.append(vacancy)
        return vacancies


if __name__ == "__main__":

    vacancy1 = Vacancy("Python разработчик", "ПАО МТС", 'https://hh.ru/vacancy/123', 100000, 'Нет опыта')
    vacancy2 = Vacancy("Data инженер", "Data Inc", 'https://hh.ru/vacancy/456', 120000, 'От 1 года до 3 лет')

    print(vacancy1)
    print(vacancy2)

    print(vacancy1 < vacancy2)  # True
    print(vacancy1 == vacancy2)  # False