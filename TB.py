from flask import flask, request
import telebot
import os

app = flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message.handler(comands=['start'])
def message_start(message):
    bot.send_messge(message.chat.id, 'Hello, user!')

@bot.message.handler(comands=['courses'])
def message_courses(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_widht=1)

    with open('courses.txt') as file:
        courses = [item.split(',') for item in file]

        for title, link in courses:
            url_button = telebot.types.InlineKeyboardButton(text=title.strip(), url=link.strip())
            keyboard.add(url_button)

        bot.send_messge(message.chat.id, 'List courses', reply_markup=keyboard)


@bot.message.handler(func=lambda x: x.text.lower().startswith('python'))
def message_courses(message):

    bot.send_messge(message.chat.id, 'Python')

@app.route('/'+ TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de.json(request.stream.read().decode("uft-8"))])
    return "Python Telegram Bot", 200

@app.route('/')
def main():
    bot.remove.webhook()
    bot.set.webhook(url='https://test-bot-ch.herokuapp.com/' + TOKEN)
    return "Python Telegram Bot", 200

if __name__ == '__main__'
    app.run(hosst='0.0.0.0', port=int(os.environ.get('PORT', 5000)))