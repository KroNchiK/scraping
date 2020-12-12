from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


# Функция парсинга заработной платы
def salary_normalization(salary):
    if salary.startswith('от'):
        min_salary = int(''.join(salary.replace('от', '').split()[0:2]))
        max_salary = None
        currency = ''.join(salary.replace('от', '').split()[2]).replace('руб.', 'RUB')
    elif salary.startswith('до'):
        min_salary = None
        max_salary = int(''.join(salary.replace('до', '').split()[0:2]))
        currency = ''.join(salary.replace('до', '').split()[2]).replace('руб.', 'RUB')
    else:
        min_salary = int(''.join(salary.split('-')[0].split()[0:2]))
        max_salary = int(''.join(salary.split('-')[1].split()[0:2]))
        currency = ''.join(salary.split('-')[1].split()[2]).replace('руб.', 'RUB')
    return min_salary, max_salary, currency


# параметр area захардкожен на Москву, можно запрашивать у пользователя, но нужно тогда подтягивать словарь соответсвия
# регионов и чилосвого соответсвия (что несколько за скопом задачи))
search_text = input('Кем хотим работать: ')
page = 0
vacancies = []
while True:
    main_link = 'https://hh.ru/search/vacancy?'
    params = {
        'area': '1',
        'text': search_text,
        'page': page
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}
    response = requests.get(main_link, headers=headers, params=params)
    soup = bs(response.text, 'html.parser')

    if response.ok:
        vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a')
            vacancy_link = vacancy_name['href']
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if salary is not None:
                min_salary, max_salary, currency = salary_normalization(salary.text)
            else:
                min_salary, max_salary, currency = None, None, None
            vacancy_data['name'] = vacancy_name.text
            vacancy_data['link'] = vacancy_link
            vacancy_data['min'] = min_salary
            vacancy_data['max'] = max_salary
            vacancy_data['currency'] = currency

            vacancies.append(vacancy_data)
    # Чекаем странички
    next_page = soup.find('a', {'data-qa': 'pager-next'})
    if next_page is None:
        break
    else:
        page += 1

pprint(vacancies)
