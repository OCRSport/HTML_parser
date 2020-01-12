import telebot
import requests
from telebot import apihelper
from bs4 import BeautifulSoup

TOKEN = '914048626:AAHRr9logyl3gUmcNXoi-Xg5gOT-V1exjjc'

proxies = {
    'http': 'http://117.1.16.132:8080',
    'https': 'http://117.1.16.132:8080',
}

apihelper.proxy = proxies

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!\nДля получения списка фильмов наберите /imdb.\nДля информации о боте наберите /help")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Бот выдает рейтинг из 250 самых популярных фильмов по версии IMDb.\nКоличество фильмов в "
                          "рейтинге иожно изменять")


@bot.message_handler(commands=['imdb'])
def get_numbers_of_films(message):
    bot.reply_to(message, "Введите количество фильмов в рейтинге\n(число от 1 до 250)")
    bot.register_next_step_handler(message, send_rating)


def send_rating(message):
    try:
        rating = int(message.text)
        if 1 <= rating <= 250:
            # не получилось сделать импорт из html_parser,
            # точнее получилось, но не смог сделать выбор числа строк рейтинга из чата, поэтому пришлось продублировать
            # зато так, кажется, быстрее работает, но это не точно)
            result = {}
            domain = 'https://www.imdb.com/'
            url = f'{domain}/chart/top'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            all_list = soup.find('tbody', class_='lister-list')
            all_films = all_list.find_all_next(class_='titleColumn')
            for film in all_films[:rating]:
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
                text = ' - '.join(i)
                # не придумал как объединить эти 2 сообщения в одно,
                # хотя так даже лучше читается, но сообщений получается в 2 раза больше,
                # а код и так не быстрый, наверно все показывать одним списком в чате будет быстрее
                bot.send_message(message.chat.id, num)
                bot.send_message(message.chat.id, text)
        else:
            bot.reply_to(message, 'Не верный ввод.\nНаберите /imdb')
    except ValueError:
        bot.reply_to(message, 'Не верный ввод.\nНаберите /imdb')


bot.polling()