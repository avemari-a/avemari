import logging
import sqlite3
from flask import Flask, request, jsonify, render_template
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Конфигурация Telegram Bot
API_TOKEN = '7296432704:AAEMD73KfNm9OMdaYM8fphlG6Jhb246ByxI'
bot = telebot.TeleBot(API_TOKEN)

# Конфигурация Flask
app = Flask(__name__)

# Логирование
logging.basicConfig(level=logging.INFO)

# Функция для получения аватара пользователя
def get_user_avatar(user_id):
    url = f"https://api.telegram.org/bot{API_TOKEN}/getUserProfilePhotos"
    params = {'user_id': user_id, 'limit': 1}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на наличие HTTP ошибок
        data = response.json()
        if data['ok'] and data['result']['total_count'] > 0:
            file_id = data['result']['photos'][0][0]['file_id']
            file_response = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/getFile?file_id={file_id}")
            file_response.raise_for_status()
            file_data = file_response.json()
            if file_data['ok']:
                file_path = file_data['result']['file_path']
                avatar_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"
                return avatar_url
    except requests.RequestException as e:
        logging.error(f"Error fetching avatar: {e}")
    return None

# Обработчик команды /start для бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No username"

    # Сохраняем пользователя в базу данных, если его там нет
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', 
                   (user_id, username))
    conn.commit()

    # Получаем аватар пользователя
    avatar_url = get_user_avatar(user_id)

    # Обновляем аватар пользователя в базе данных
    if avatar_url:
        cursor.execute('UPDATE users SET avatar_url=? WHERE user_id=?', (avatar_url, user_id))
        conn.commit()

    conn.close()

    # Подготавливаем данные для mini-app
    user_data = {
        "user_id": user_id,
        "username": username,
        "avatar_url": avatar_url or '/static/default_avatar.png'
    }

    # Передаем данные mini-app через WebAppInfo
    markup = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url='https://avemari.vercel.app/')  # Замените на ваш URL
    btn = InlineKeyboardButton('Open Mini App', web_app=web_app_info)
    markup.add(btn)
    bot.send_message(message.chat.id, "Welcome! Your data is ready.", reply_markup=markup)

# Маршрут для получения аватара пользователя
@app.route('/get_avatar', methods=['POST'])
def get_avatar():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "User ID is missing"}), 400

    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    cursor.execute('SELECT avatar_url FROM users WHERE user_id=?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user and user[0]:
        return jsonify({"status": "success", "avatar_url": user[0]})
    else:
        return jsonify({"status": "error", "message": "Avatar not found"}), 404

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    # Создание таблицы пользователей с полем для аватара
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

def get_db_connection():
    conn = sqlite3.connect('notcoin.db')
    conn.row_factory = sqlite3.Row
    return conn

# Основной маршрут
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для регистрации пользователя
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    
    if not user_id or not username:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    # Вставляем пользователя, если его нет в базе
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', 
                   (user_id, username))
    conn.commit()

    # Получение текущего количества монет
    cursor.execute('SELECT coins FROM users WHERE user_id=?', (user_id,))
    coins = cursor.fetchone()
    conn.close()
    
    return jsonify({'status': 'success', 'points': coins[0] if coins else 0})

# Запуск Flask приложения и Telegram бота
if __name__ == '__main__':
    init_db()  # Инициализируем базу данных при запуске
    import threading
    threading.Thread(target=bot.polling).start()
    app.run(debug=True)
