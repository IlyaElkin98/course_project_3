import requests


class API:
    """
    Класс для получения данных о компаниях и вакансиях с сайта hh.ru через API.
    Использует response.json() для парсинга ответов.
    """

    def __init__(self):
        self.vacancies = []
        self.employers = []

    def get_companies_and_vacancies_count(self):
        i = 1
        j = 15
        while i < j:
            try:
                response = requests.get(f"https://api.hh.ru/employers/{i}")
                response.raise_for_status()
                data = response.json()
                if data.get("open_vacancies", 0) > 0:
                    self.employers.append([data["id"], data["name"], data["open_vacancies"]])
                i += 1
            except (requests.RequestException, KeyError):
                i += 1
                j += 1

        try:
            response = requests.get("https://api.hh.ru/employers/1740")
            response.raise_for_status()
            data = response.json()
            self.employers.append([data["id"], data["name"], data["open_vacancies"]])
        except (requests.RequestException, KeyError):
            pass

        return self.employers

    def get_all_vacancies(self):
        params = {
            "employer_id": [employer[0] for employer in self.employers],
            "area": 113,
            "per_page": 100,
        }
        for page in range(10):
            params["page"] = page
            try:
                response = requests.get("https://api.hh.ru/vacancies", params=params)
                response.raise_for_status()
                vacancies_items = response.json().get("items", [])
                for item in vacancies_items:
                    salary = item.get("salary")
                    salary_value = None
                    if salary:
                        salary_value = salary.get("from") or salary.get("to")
                    self.vacancies.append([
                        item.get("name"),
                        item.get("apply_alternate_url"),
                        salary_value,
                        item.get("employer", {}).get("id"),
                    ])
            except requests.RequestException:
                continue

        return self.vacancies