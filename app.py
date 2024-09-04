from flask import Flask, request, jsonify, render_template
import sqlite3
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Конфигурация Telegram Bot
API_TOKEN = '7296432704:AAEMD73KfNm9OMdaYM8fphlG6Jhb246ByxI'
bot = telebot.TeleBot(API_TOKEN)
TELEGRAM_BOT_TOKEN = '7296432704:AAEMD73KfNm9OMdaYM8fphlG6Jhb246ByxI'



# Конфигурация Flask
app = Flask(__name__)

def get_user_avatar(user_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUserProfilePhotos"
    params = {
        'user_id': user_id,
        'limit': 1  # Ограничиваем количество фото, чтобы получить только последнее
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['ok'] and data['result']['total_count'] > 0:
        # Берем первое фото из списка
        file_id = data['result']['photos'][0][0]['file_id']
        
        # Получаем URL файла с помощью getFile
        file_response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}")
        file_data = file_response.json()
        
        if file_data['ok']:
            file_path = file_data['result']['file_path']
            avatar_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
            return avatar_url
    
    return None  # Если аватар не найден

@app.route('/get_avatar', methods=['POST'])
def get_avatar():
    user_id = request.json.get('user_id')
    avatar_url = get_user_avatar(user_id)
    
    if avatar_url:
        return jsonify({"status": "success", "avatar_url": avatar_url})
    else:
        return jsonify({"status": "error", "message": "Avatar not found"}), 404

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY, 
            username TEXT,
            coins INTEGER DEFAULT 0
        )
    ''')
    # Создание таблицы для рефералов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            user_id INTEGER,
            referral_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (referral_id) REFERENCES users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('notcoin.db')
    conn.row_factory = sqlite3.Row
    return conn

# Flask маршруты
@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/click', methods=['POST'])
def click():
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET coins = coins + 1 WHERE user_id=?', (user_id,))
    conn.commit()
    
    cursor.execute('SELECT coins FROM users WHERE user_id=?', (user_id,))
    coins = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'status': 'success', 'coins': coins})

@app.route('/earn_coins', methods=['POST'])
def earn_coins():
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET coins = coins + 1 WHERE user_id=?', (user_id,))
    conn.commit()
    
    cursor.execute('SELECT coins FROM users WHERE user_id=?', (user_id,))
    coins = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'status': 'success', 'coins': coins})

@app.route('/invite', methods=['POST'])
def invite():
    data = request.json
    user_id = data.get('user_id')
    friend_username = data.get('friend_username')
    
    if not user_id or not friend_username:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM users WHERE username=?', (friend_username,))
    friend = cursor.fetchone()
    
    if friend:
        friend_id = friend[0]
        cursor.execute('INSERT INTO referrals (user_id, referral_id) VALUES (?, ?)', (user_id, friend_id))
        cursor.execute('UPDATE users SET coins = coins + 2500 WHERE user_id=?', (user_id,))
        cursor.execute('UPDATE users SET coins = coins + 2500 WHERE user_id=?', (friend_id,))
        conn.commit()
        
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Friend invited successfully'})

# Обработчик команды /start для бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No username"

    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', 
                   (user_id, username))
    conn.commit()
    conn.close()

    markup = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url='https://avemari.vercel.app/')
    btn = InlineKeyboardButton('Open Mini App', web_app=web_app_info)
    markup.add(btn)
    bot.send_message(message.chat.id, "Welcome! Click the button below to open the mini app.", reply_markup=markup)

# Запуск Flask приложения и Telegram бота
if __name__ == '__main__':
    init_db()  # Инициализируем базу данных при запуске
    import threading
    threading.Thread(target=bot.polling).start()
    app.run(debug=True)
