import unittest
from unittest.mock import patch, MagicMock
from src.iteraction_api import API


class TestAPI(unittest.TestCase):

    @patch('src.iteraction_api.requests.get')
    def test_get_companies_and_vacancies_count(self, mock_get):
        def side_effect(url, *args, **kwargs):
            id_str = url.split('/')[-1]
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            if id_str == '1740':
                mock_resp.json.return_value = {"id": 1740, "name": "Test Employer 1740", "open_vacancies": 5}
            else:
                try:
                    i = int(id_str)
                except ValueError:
                    i = 0
                if i < 15:
                    mock_resp.json.return_value = {"id": i, "name": f"Employer {i}", "open_vacancies": 3 if i % 2 == 0 else 0}
                else:
                    mock_resp.status_code = 404
                    mock_resp.json.return_value = {}
            return mock_resp

        mock_get.side_effect = side_effect

        api = API()
        employers = api.get_companies_and_vacancies_count()

        expected_ids = [i for i in range(2, 15, 2)] + [1740]
        actual_ids = [e[0] for e in employers]
        self.assertListEqual(actual_ids, expected_ids)

    @patch('src.iteraction_api.requests.get')
    def test_get_all_vacancies(self, mock_get):
        api = API()
        api.employers = [[1, "Employer 1", 5], [2, "Employer 2", 3]]

        vacancies_data = {
            "items": [
                {
                    "name": "Vacancy 1",
                    "apply_alternate_url": "http://example.com/vac1",
                    "salary": {"from": 1000, "to": 2000},
                    "employer": {"id": 1}
                },
                {
                    "name": "Vacancy 2",
                    "apply_alternate_url": "http://example.com/vac2",
                    "salary": None,
                    "employer": {"id": 2}
                }
            ]
        }
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = vacancies_data
        mock_get.return_value = mock_resp

        vacancies = api.get_all_vacancies()

        self.assertTrue(any(v[0] == "Vacancy 1" for v in vacancies))
        self.assertTrue(any(v[0] == "Vacancy 2" for v in vacancies))


if __name__ == '__main__':
    unittest.main()