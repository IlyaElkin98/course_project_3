from src.bd_manager import DBManager

print('''Привет! 
Эта программа создает базу данных Postgresql
с краткой информацией о вакансиях и компаниях, полученной при помощи API hh.ru.
Для продолжения работы введите номер интересующего запроса\n''')

dbmanage = DBManager()

if dbmanage.check() is True:
    print('Создаем базу данных подождите немного...\n')
    dbmanage.create_tables()
    dbmanage.get_companies_and_vacancies_count()
    dbmanage.get_all_vacancies()
    dbmanage.to_postgresql('employers')
    dbmanage.to_postgresql('vacancies')

try:
    print('''    1 - получить среднюю зарплату по полученным вакансиям
    2 - получить вакансии с зарплатой выше средней
    3 - найти вакансии с ключевым словом в названии
    4 - вывести все компании
    5 - вывести все вакансии, предоставляемые полученными работодателями 
    6 - выйти\n''')

    while True:
        req = int(input("Введите номер опции:"))
        if req == 1:
            dbmanage.get_avg_salary()
        elif req == 2:
            dbmanage.get_vacancies_with_higher_salary()
        elif req == 3:
            try:
                key_word = input('\nВведите ключевое слово: ')
                dbmanage.get_vacancies_with_keyword(key_word)
            except:
                print('\nВакансии не найдены')
        elif req == 4:
            dbmanage.print_employers()
        elif req == 5:
            dbmanage.print_vacancies()
        elif req == 6:
            print('Завершение работы')
            break
        else:
            print('\n\nВведен некорректный номер запроса, попробуй еще раз... ')
            req = int(input())

        print('\nЕсли интересует что-то еще, можете ввести еще один запрос, либо выйти (6)')
except:
    print("введены неправильные данные для подключения к БД")