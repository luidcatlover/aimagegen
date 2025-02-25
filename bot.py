import telebot
from telebot import types
from logic import Text2ImageAPI
from config import TOKEN, SECRET_TOKEN, API_TOKEN
import os


bot = telebot.TeleBot(token=TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Yo! To generate image type /generate (request). Example /generate black men fight with coconuts')

@bot.message_handler(commands=['generate'])
def generate_image(message):
    try:
        promt = message.text.replace('/generate ', '')
        msg = bot.reply_to(message, 'Генерация изображения..')

        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_TOKEN, SECRET_TOKEN)
        model_id = api.get_model()
        uuid = api.generate(promt, model_id)
        images = api.check_generation(uuid)[0]

        api.save_image(images, 'result.jpg')

        bot.delete_message(msg.chat.id, msg.message_id)

        with open('result.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo=photo)

        os.remove('result.jpg')
    except Exception as err:
        bot.send_message(message.chat.id, f'Возникла ошибка при генерации изображения: {err}')

bot.infinity_polling()
