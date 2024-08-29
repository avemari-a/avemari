import telebot
import sqlite3
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

API_TOKEN = '7296432704:AAEMD73KfNm9OMdaYM8fphlG6Jhb246ByxI'
bot = telebot.TeleBot(API_TOKEN)

# Функция для получения URL аватара пользователя
def get_user_avatar(user_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getUserProfilePhotos?user_id={user_id}"
    response = requests.get(url).json()
    
    if response['ok'] and response['result']['total_count'] > 0:
        file_id = response['result']['photos'][0][0]['file_id']
        file_info_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
        file_info_response = requests.get(file_info_url).json()
        
        if file_info_response['ok']:
            file_path = file_info_response['result']['file_path']
            return f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
    return None

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY, 
            username TEXT,
            avatar_url TEXT,
            coins INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No username"
    bot_token = API_TOKEN

    # Получение URL аватара
    avatar_url = get_user_avatar(user_id, bot_token) or 'default_avatar.png'

    # Сохранение данных пользователя в базу данных
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, avatar_url) VALUES (?, ?, ?)', 
                   (user_id, username, avatar_url))
    conn.commit()
    conn.close()

    # Отправка сообщения с кнопкой для открытия mini app
    markup = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url='https://avemari-avemari-as-projects.vercel.app/')
    btn = InlineKeyboardButton('Open Mini App', web_app=web_app_info)
    markup.add(btn)
    bot.send_message(message.chat.id, "Welcome! Click the button below to open the mini app.", reply_markup=markup)

# Инициализируем базу данных при запуске
init_db()

# Запуск бота
bot.polling()
