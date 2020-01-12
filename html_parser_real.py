import requests
import pprint
from bs4 import BeautifulSoup

domain = 'https://www.imdb.com/'
url = f'{domain}/chart/top'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.h1.text)

k = 5  # количество фильмов в списке (возможно от 1 до 250)
result = {}
all_list = soup.find('tbody', class_='lister-list')
all_films = all_list.find_all_next(class_='titleColumn')
for film in all_films[:k]:
    text_href_tag = film.find('a')
    text = text_href_tag.text
    href = text_href_tag.get('href')
    url = f'{domain}{href}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scores_tag = soup.find_all('span', itemprop="ratingValue")
    for score in scores_tag:
        result[text] = score.text
result_list = list(result.items())
result_list.sort(key=lambda i: i[1], reverse=True)
num = 0
for i in result_list:
    num += 1
    print(num, '-', i[0], ':', i[1])
# pprint.pprint(result)
