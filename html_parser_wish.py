import requests
import pprint
from bs4 import BeautifulSoup

domain = 'https://www.imdb.com/'
url = f'{domain}/chart/top'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.h1.text)

result_films = []
result_scores = []
all_list = soup.find('div', class_='lister')
all_films = all_list.find_all_next('td', class_='titleColumn')
all_scores = all_list.find_all_next('td', class_='ratingColumn imdbRating')
for all_film in all_films[:10]:
    result_films.append(all_film.text)
for all_score in all_scores[:10]:
    result_scores.append(all_score.text)
result = list(map(list, zip(result_films, result_scores)))
pprint.pprint(result)

