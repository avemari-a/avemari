from flask import Flask, request, jsonify, render_template
import sqlite3
import requests

app = Flask(__name__)

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY, 
            username TEXT,
            avatar_url TEXT,
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

# Функция для получения URL аватара пользователя
def get_user_avatar(user_id):
    url = f"https://api.telegram.org/bot7296432704:AAEMD73KfNm9OMdaYM8fphlG6Jhb246ByxI/getUserProfilePhotos?user_id={user_id}"
    response = requests.get(url).json()
    
    if response['ok'] and response['result']['total_count'] > 0:
        file_id = response['result']['photos'][0][0]['file_id']
        file_info_url = f"https://api.telegram.org/bot7296432704:AAEMD73KfNm9OMdaYM8fphlG6Jhb246ByxI/getFile?file_id={file_id}"
        file_info_response = requests.get(file_info_url).json()
        
        if file_info_response['ok']:
            file_path = file_info_response['result']['file_path']
            return f"https://api.telegram.org/file/bot7296432704:AAEMD73KfNm9OMdaYM8fphlG6Jhb246ByxI/{file_path}"
    return None

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для регистрации пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_id = data['user_id']
    username = data.get('username', 'Unknown')

    # Получение URL аватара
    avatar_url = get_user_avatar(user_id)
    
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    # Вставляем пользователя, если его нет в базе
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, avatar_url) VALUES (?, ?, ?)', 
                   (user_id, username, avatar_url))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'User registered successfully'})

# Маршрут для начисления монет при клике
@app.route('/click', methods=['POST'])
def click():
    data = request.json
    user_id = data['user_id']
    
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    # Увеличиваем количество монет на 1
    cursor.execute('UPDATE users SET coins = coins + 1 WHERE user_id=?', (user_id,))
    conn.commit()
    
    # Получаем обновленное количество монет
    cursor.execute('SELECT coins FROM users WHERE user_id=?', (user_id,))
    coins = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'status': 'success', 'coins': coins})

# Маршрут для начисления монет в другой ситуации
@app.route('/earn_coins', methods=['POST'])
def earn_coins():
    data = request.json
    user_id = data['user_id']
    
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    # Начисляем монеты
    cursor.execute('UPDATE users SET coins = coins + 1 WHERE user_id=?', (user_id,))
    conn.commit()
    
    # Получаем количество монет
    cursor.execute('SELECT coins FROM users WHERE user_id=?', (user_id,))
    coins = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'status': 'success', 'coins': coins})

# Маршрут для приглашения друзей
@app.route('/invite', methods=['POST'])
def invite():
    data = request.json
    user_id = data['user_id']
    friend_username = data['friend_username']
    
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    
    # Ищем друга в базе данных по username
    cursor.execute('SELECT user_id FROM users WHERE username=?', (friend_username,))
    friend = cursor.fetchone()
    
    if friend:
        friend_id = friend[0]
        # Добавляем запись в таблицу рефералов
        cursor.execute('INSERT INTO referrals (user_id, referral_id) VALUES (?, ?)', (user_id, friend_id))
        # Начисляем монеты за приглашение
        cursor.execute('UPDATE users SET coins = coins + 2500 WHERE user_id=?', (user_id,))
        cursor.execute('UPDATE users SET coins = coins + 2500 WHERE user_id=?', (friend_id,))
        conn.commit()
        
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Friend invited successfully'})

# Запуск приложения
if __name__ == '__main__':
    init_db()  # Инициализируем базу данных при запуске
    app.run(debug=True)
