# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Будем получать список праздников в конкретной стране за определённый год
import requests
from pprint import pprint

main_link = 'https://calendarific.com/api/v2/holidays'
api_key = 'c8365f7019045624671c11235bdc4e38a82da69d'
country = 'RU'
year = '2021'
url_params = {
    'api_key': api_key,
    'country': country,
    'year': year
}
outfile = 'holidays.json'

response = requests.get(main_link, params=url_params)

if response.ok:
    j_data = response.json()
    with open(outfile, 'w') as out:
        pprint(j_data, out)
