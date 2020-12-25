import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint
import unicodedata

# Функция добавляющая новости в БД
def update_db(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client['news']
    lenta = db.lenta
    for item in data:
        lenta.update_one({'link': item['link']}, {'$set': item}, upsert=True)

url = 'https://lenta.ru'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/87.0.4280.88 Safari/537.36'}

items_xpath = "//div[@class='span4']/div[@class='first-item'] | //div[@class='span4']/div[@class='item']"

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

raw_items = dom.xpath(items_xpath)
all_news = []
for item in raw_items:
    data_news = {}
    text = unicodedata.normalize('NFKD', item.xpath("./h2/a/text() | ./a/text()")[0])
    date = item.xpath(".//time/@title")[0]
    link = url + item.xpath(".//a/@href")[0]
    data_news['text'] = text
    data_news['source'] = 'lenta.ru'
    data_news['date'] = date
    data_news['link'] = link
    all_news.append(data_news)

update_db(all_news)
pprint(all_news)

# В идеале, стоит привести время к единому стандарту для всех источников