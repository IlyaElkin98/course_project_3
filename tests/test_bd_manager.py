import unittest
from unittest.mock import patch, MagicMock
from src.bd_manager import DBManager  # замените на реальный путь к вашему DBManager


class TestDBManager(unittest.TestCase):

    @patch('src.bd_manager.psycopg2.connect')
    def test_get_vacancies_with_higher_salary_prints_rows(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            ("Vacancy A", 3000, "urlA"),
            ("Vacancy B", 4000, "urlB"),
        ]

        db = DBManager()

        with patch('builtins.print') as mock_print:
            db.get_vacancies_with_higher_salary()

            expected_calls = [
                unittest.mock.call(
                    "Название вакансии - Vacancy A\nЗарплата - 3000\nСсылка - urlA\n"
                ),
                unittest.mock.call(
                    "Название вакансии - Vacancy B\nЗарплата - 4000\nСсылка - urlB\n"
                ),
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)

        mock_conn.close.assert_called_once()

    @patch('src.bd_manager.psycopg2.connect')
    def test_get_vacancies_with_keyword_prints_rows(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            ("Vacancy 1", "url1", 1000, 1),
            ("Vacancy 2", "url2", 2000, 2),
        ]

        db = DBManager()

        with patch('builtins.print') as mock_print:
            db.get_vacancies_with_keyword("Developer")
            mock_print.assert_any_call(("Vacancy 1", "url1", 1000, 1))
            mock_print.assert_any_call(("Vacancy 2", "url2", 2000, 2))

        mock_conn.close.assert_called_once()

    @patch('src.bd_manager.psycopg2.connect')
    def test_check_returns_true_on_exception(self, mock_connect):
        mock_connect.side_effect = Exception("Connection failed")

        db = DBManager()
        self.assertTrue(db.check())

    @patch('src.bd_manager.psycopg2.connect')
    def test_print_employers(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            (1, "Employer 1", 5),
            (2, "Employer 2", 10),
        ]

        db = DBManager()

        with patch('builtins.print') as mock_print:
            db.print_employers()
            expected_calls = [
                unittest.mock.call("id - 1\nНазвание компании - Employer 1\nКоличество открытых вакансий - 5\n"),
                unittest.mock.call("id - 2\nНазвание компании - Employer 2\nКоличество открытых вакансий - 10\n"),
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)

        mock_conn.close.assert_called_once()

    @patch('src.bd_manager.psycopg2.connect')
    def test_print_vacancies(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            ("Vacancy 1", "url1", 1000, 1),
            ("Vacancy 2", "url2", 2000, 2),
        ]

        db = DBManager()

        with patch('builtins.print') as mock_print:
            db.print_vacancies()
            expected_calls = [
                unittest.mock.call("Название вакансии - Vacancy 1\nСсылка - url1\nЗарплата - 1000\nid работодателя - 1\n"),
                unittest.mock.call("Название вакансии - Vacancy 2\nСсылка - url2\nЗарплата - 2000\nid работодателя - 2\n"),
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)

        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()