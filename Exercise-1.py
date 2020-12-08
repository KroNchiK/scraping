# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
from pprint import pprint

username = 'Netflix'
count = '100'
main_link = f'https://api.github.com/users/{username}/repos?per_page={count}'
headers = {'Accept': 'application/vnd.github.v3+json'}
outfile = 'repo_list.json'

response = requests.get(main_link, headers=headers)

if response.ok:
    j_data = response.json()
    with open(outfile, 'w') as out:
        pprint(j_data, out)
