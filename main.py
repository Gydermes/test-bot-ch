from flask import Flask, request
import telebot
import os
from telebot import types


app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def message_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот m".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(commands=['List'])
def message_courses(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    with open('courses.txt') as file:
        courses = [item.split(',') for item in file]

        for title, link in courses:
            url_button = telebot.types.InlineKeyboardButton(text=title.strip(), url=link.strip())
            keyboard.add(url_button)

        bot.send_message(message.chat.id, 'List of courses', reply_markup=keyboard)


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot 30-01-2022", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://test-bot-che.herokuapp.com/' + TOKEN)
    return 'Python Telegram Bot', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
