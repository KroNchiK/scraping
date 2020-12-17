# Ищем и выводим на экран вакансии с заработной платой больше введённой суммы

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
hh = db.hh

salary = float(input('Введите размер ЗП: '))
currency = input('Введите валюту (RUB/USD): ')

for vacancy in hh.find({'$and': [{'$or': [{'min': {'$gt': salary}}, {'max': {'$gt': salary}}]},
                                 {'currency': currency}]}):
    pprint(vacancy)