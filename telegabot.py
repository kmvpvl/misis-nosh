import telebot
from telebot import types
import codecs
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("token")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='1', callback_data='1')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='2', callback_data='2')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='3', callback_data='3')
    keyboard.add(key_3)
    bot.send_photo(message.chat.id, photo=open('map.jpg', 'rb'),  reply_markup=keyboard,
                   caption=f'Привет, {message.from_user.first_name}!\n\n'
                           f'Проголодался? Здесь, ты легко и быстро получишь информацию о ближайших местах питания возле МИСИС\n\n'
                           f'Перед тобой три локации, выбери ту, в которой ты хочешь покушать\n\nПриятного аппетита!')


@bot.callback_query_handler(func=lambda call: True)
def my_button(call):
    if len(call.data) == 1:
        location_choice(call)
    elif call.data[-1].isdigit():
        cafe_choice(call)
    else:
        param_choice(call)


def location_choice(call):
    keyboard = types.InlineKeyboardMarkup()
    mess = "Держи список заведений и выбери понравившееся, чтобы узнать больше информации о нем!\n" + \
           codecs.open(call.data+"loc/data.txt", encoding='utf-8').read()
    if call.data == "1":
        for i in range(5):
            keyboard.add(types.InlineKeyboardButton(text=str(i+1), callback_data="1loc/"+str(i+1)))
    elif call.data == "2":
        for i in range(10):
            keyboard.add(types.InlineKeyboardButton(text=str(i+1), callback_data="2loc/"+str(i+1)))
    elif call.data == "3":
        for i in range(9):
            keyboard.add(types.InlineKeyboardButton(text=str(i+1), callback_data="3loc/"+str(i+1)))
    bot.send_message(call.message.chat.id, mess, reply_markup=keyboard)


def cafe_choice(call):
    ind = call.data.find('/')
    names = codecs.open(call.data[:ind+1] + "data.txt", encoding='utf-8').readlines()
    name = names[int(call.data[ind+1:])-1]
    keyboard = types.InlineKeyboardMarkup()
    key_address = types.InlineKeyboardButton(text="Адрес", callback_data=call.data+"adrs")
    key_time = types.InlineKeyboardButton(text="Время работы", callback_data=call.data+"time")
    key_menu = types.InlineKeyboardButton(text="Меню", callback_data=call.data+"menu")
    keyboard.add(key_address)
    keyboard.add(key_time)
    keyboard.add(key_menu)
    bot.send_photo(call.message.chat.id, photo=open(call.data+".jpg", 'rb'),  reply_markup=keyboard,
                   caption=f'{name}Что бы ты хотел узнать?')


def param_choice(call):
    if call.data[-4:] == 'adrs':
        bot.send_message(call.message.chat.id,
                         codecs.open(call.data[:-4]+'.txt', encoding='utf-8').readlines()[0])
    elif call.data[-4:] == 'time':
        bot.send_message(call.message.chat.id,
                         ''.join(codecs.open(call.data[:-4] + '.txt', encoding='utf-8').readlines()[1:-1]))
    elif call.data[-4:] == 'menu':
        bot.send_message(call.message.chat.id,
                         codecs.open(call.data[:-4]+'.txt', encoding='utf-8').readlines()[-1])


@bot.message_handler(content_types=['text'])
def start_function(message):
    bot.send_message(message.chat.id, f'Напишите /start')


def function_who(message):
    print(message.chat.id, message.text)


bot.infinity_polling()

if __name__ == '__main__':
    bot.polling(none_stop=True)
