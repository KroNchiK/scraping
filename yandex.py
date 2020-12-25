import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

# Функция добавляющая новости в БД
def update_db(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client['news']
    yandex = db.yandex
    for item in data:
        yandex.update_one({'link': item['link']}, {'$set': item}, upsert=True)

url = 'https://yandex.ru/news/'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/87.0.4280.88 Safari/537.36'}
items_xpath = "//div[contains(@class, 'news-top-stories')]//div[contains(@class, 'mg-grid__col')]"

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

raw_items = dom.xpath(items_xpath)
all_news = []
for item in raw_items:
    data_news = {}
    text = item.xpath(".//h2[@class='mg-card__title']/text()")[0]
    source = item.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]
    link = item.xpath(".//span[@class='mg-card-source__source']/a/@href")[0]
    date = item.xpath(".//span[@class='mg-card-source__time']/text()")[0]
    data_news['text'] = text
    data_news['source'] = source
    data_news['link'] = link
    data_news['date'] = date
    all_news.append(data_news)

update_db(all_news)
pprint(all_news)

# В идеале, стоит привести время к единому стандарту для всех источников