from flask import Flask, request
import telebot
import types
import os

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот Gydermesa".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, text="Привеет.. Спасибо что читаешь статью!)")
    elif message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif message.text == "Как меня зовут?":
        bot.send_message(message.chat.id, "У меня нет имени..")

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Поздороваться с читателями")

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


bot.polling(none_stop=True)


@bot.message_handler(commands=['List'])
def message_courses(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

    with open('courses.txt') as file:
        courses = [item.split(',') for item in file]

        for title, link in courses:
            url_button = telebot.types.InlineKeyboardButton(text=title.strip(), url=link.strip())
            keyboard.add(url_button)

        bot.send_message(message.chat.id, 'List of saits', reply_markup=keyboard)


@bot.message_handler(func=lambda x: x.text.lower().startswith('python'))
def message_text(message):
    bot.send_message(message.chat.id, 'Python')


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
