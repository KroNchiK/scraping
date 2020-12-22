import requests
from lxml import html
from pprint import pprint
import unicodedata

header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/87.0.4280.88 Safari/537.36'}

# lenta.ru
lenta_url = 'https://lenta.ru/'
lenta_xpath = "//div[@class='first-item']/h2/a/text()  | //div[@class='item']/a/text()"





response = requests.get(lenta_url, headers=header)
dom = html.fromstring(response.text)

row_news = dom.xpath(lenta_xpath)
all_news = []
for news in row_news:
    data_news = {}
    news = unicodedata.normalize('NFKD', news)
    data_news['news'] = news
    data_news['source'] = 'lenta.ru'
    all_news.append(data_news)

pprint(all_news)