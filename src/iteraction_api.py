import json

import requests


class API:
    """
    Класс for_API создан для получения данных о компаниях и вакансиях с сайта hh.ru посредством API ключа.
    """

    def __init__(self):
        self.vacancies = []
        self.employers = []

    def get_companies_and_vacancies_count(self):
        """Метод выводящий информацию о компаниях и их доступных вакансий"""
        i = 1
        j = 15
        while i < j:
            req = requests.get("https://api.hh.ru/employers/" + str(i))
            data = req.content.decode()
            req.close()
            jo = json.loads(data)
            try:
                if jo["open_vacancies"] > 0 and jo["open_vacancies"] is not None:
                    self.employers.append([jo["id"], jo["name"], jo["open_vacancies"]])
                    i += 1
                    continue
                i += 1
                j += 1
            except:
                i += 1
                j += 1
        req = requests.get("https://api.hh.ru/employers/" + str(1740))
        data = req.content.decode()
        req.close()
        jo = json.loads(data)
        self.employers.append([jo["id"], jo["name"], jo["open_vacancies"]])
        return self.employers

    def get_all_vacancies(self):
        """Метод выводящий данные о вакансиях"""
        params = {
            "employer_id": [],
            "area": 113,
            "per_page": 100,  # Кол-во вакансий на 1 странице
        }
        for i in self.employers:
            params["employer_id"].append(i[0])
        for page in range(0, 10):
            params["page"] = page
            req = requests.get("https://api.hh.ru/vacancies", params)
            data = req.content.decode()
            req.close()
            data = json.loads(data)["items"]
            for i in data:
                try:
                    if i["salary"]["from"] is None:
                        self.vacancies.append(
                            [
                                i["name"],
                                i["apply_alternate_url"],
                                i["salary"]["to"],
                                i["employer"]["id"],
                            ]
                        )
                    else:
                        self.vacancies.append(
                            [
                                i["name"],
                                i["apply_alternate_url"],
                                i["salary"]["from"],
                                i["employer"]["id"],
                            ]
                        )
                except:
                    self.vacancies.append(
                        [
                            i["name"],
                            i["apply_alternate_url"],
                            i["salary"],
                            i["employer"]["id"],
                        ]
                    )
        return self.vacancies
