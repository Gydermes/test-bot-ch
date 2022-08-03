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
    btn1 = types.KeyboardButton("Динамо")
    btn2 = types.KeyboardButton("Football UA")
    btn3 = types.KeyboardButton("Корреспондент")
    btn4 = types.KeyboardButton("Gismeteo")
    btn5 = types.KeyboardButton("не нажимай")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот Yaroslava".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "Динамо":
        bot.send_message(message.chat.id, "http://dynamo.kiev.ua/", reply_markup=markup)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
    elif message.text == "Football UA":
        bot.send_message(message.chat.id, "https://football.ua/", reply_markup=markup)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)

    elif message.text == "Корреспондент":
        bot.send_message(message.chat.id, "https://ua.korrespondent.net/", reply_markup=markup)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)

    elif message.text == "Gismeteo":
        bot.send_message(message.chat.id, "https://www.gismeteo.ua/weather-chuhuiv-12830/weekly/", reply_markup=markup)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)

    elif message.text == "не нажимай":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 зачем ти нажал!!!")
        markup.add(button1)
        bot.send_message(message.chat.id, text="BLOCKED", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")





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
