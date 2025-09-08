import os
from typing import Any

from dotenv import load_dotenv

from src.iteraction_api import API
import psycopg2



class DBManager(API):
    """
    Класс DBManager создан для работы с базой данных, основанной на данных, полученных с сайта hh.ru.
    В нем реализована централизованное хранение request'ов в базе данных Postgresql.

    Методы:
    create_tables - создание 2 таблиц для работодателей и вакансий
    to_postgresql - заполнение таблиц полученными данными
    get_avg_salary - расчет средней зарплаты
    get_vacancies_with_higher_salary - вывод самой высокой зарплаты
    get_vacancies_with_keyword - поиск по ключевому слову
    """

    def __init__(self):
        """Конструктор принимает переменные для работы с базой данных"""
        load_dotenv()  # Загружает переменные из .env в окружение
        super().__init__()
        self.db = os.environ.get('DB_NAME')
        self.user = os.environ.get('DB_USER')
        self.pswd = os.environ.get('DB_PASSWORD')
        self.port = int(os.environ.get('DB_PORT', 5432))  # Порт по умолчанию 5432

        self.connect = None

    def con(self):
        """Метод подключения экземпляра к базе данных"""
        self.connect = psycopg2.connect(
            database=self.db, user=self.user, password=self.pswd, port=self.port
        )

    def create_tables(self):
        """Метод создания таблицы"""
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute(
                        """drop table if exists vacancies;
                                drop table if exists employers;
                                create table vacancies (
                                    vac_name varchar NOT NULL,
                                    url varchar NOT NULL,
                                    salary int,
                                    emp_id int
                                );

                                create table employers (
                                    emp_id int unique NOT NULL,
                                    emp_name varchar NOT NULL,
                                    emp_open_vac int
                                );"""
                    )
        finally:
            self.connect.close()

    def to_postgresql(self, tab_name: str):
        """Метод добавления вакансий и работодателей"""
        # try:
        self.con()
        with self.connect:
            with self.connect.cursor() as cur:
                if tab_name == "vacancies":
                    for tabs_info in self.vacancies:
                        cur.execute(
                            f"insert into {tab_name} values (%s, %s, %s, %s)",
                            (tabs_info[0], tabs_info[1], tabs_info[2], tabs_info[3]),
                        )
                elif tab_name == "employers":
                    for tabs_info in self.employers:
                        cur.execute(
                            f"insert into {tab_name} values (%s, %s, %s)",
                            (tabs_info[0], tabs_info[1], tabs_info[2]),
                        )
        # finally:
        self.connect.close()

    def get_avg_salary(self):
        """Метод расчета средней заработной платы"""
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute("select avg(salary) from vacancies;")
                    rows = cur.fetchall()
                    for row in rows:
                        avg = float(row[0])
                        print(round(avg, 2))
        finally:
            self.connect.close()

    def get_vacancies_with_higher_salary(self):
        """Метод вывода самой высокой зарплаты"""
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute(
                        "SELECT vac_name, salary, url FROM vacancies WHERE salary > (SELECT AVG(salary) FROM "
                        "vacancies);"
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        print(
                            f"""Название вакансии - {row[0]}
Зарплата - {row[1]}
Ссылка - {row[2]}\n"""
                        )
        finally:
            self.connect.close()

    def get_vacancies_with_keyword(self, key_word: str) -> Any:
        """Метод поиска по ключевому слову"""
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM vacancies WHERE vac_name LIKE %s",
                        (f"%{key_word}%",),
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        finally:
            self.connect.close()

    def check(self):
        """Метод, который позволяет выполнять SQL-запросы вакансий к базе данных"""
        try:
            self.con()
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies")
                    rows = cur.fetchall()
                    if len(rows) > 0:
                        return False
                    return True
        except:
            return True

    def print_employers(self) -> None:
        """Метод, который позволяет выполнять SQL-запросы работодателей к базе данных"""
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute("SELECT * FROM employers")
                    rows = cur.fetchall()
                    for row in rows:
                        print(
                            f"""id - {row[0]}
Название компании - {row[1]}
Количество открытых вакансий - {row[2]}\n"""
                        )
        finally:
            self.connect.close()

    def print_vacancies(self) -> None:
        """Метод, который позволяет выполнять SQL-запросы вакансий к базе данных"""
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies")
                    rows = cur.fetchall()
                    for row in rows:
                        print(
                            f"""Название вакансии - {row[0]}
Ссылка - {row[1]}
Зарплата - {row[2]}
id работодателя - {row[3]}\n"""
                        )
        finally:
            self.connect.close()
