import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

API_TOKEN = '7296432704:AAEMD73KfNm9OMdaYM8fphlG6Jhb246ByxI'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url='https://avemari-avemari-as-projects.vercel.app/')
    btn = InlineKeyboardButton('Open Mini App', web_app=web_app_info)
    markup.add(btn)
    bot.send_message(message.chat.id, "Welcome! Click the button below to open the mini app.", reply_markup=markup)

bot.polling()
