from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    user_id = request.form['user_id']
    username = request.form['username']
    
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'User registered successfully'})

@app.route('/click', methods=['POST'])
def click():
    user_id = request.form['user_id']
    
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET coins = coins + 1 WHERE user_id=?', (user_id,))
    conn.commit()
    
    cursor.execute('SELECT coins FROM users WHERE user_id=?', (user_id,))
    coins = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'status': 'success', 'coins': coins})

@app.route('/earn_coins', methods=['POST'])
def earn_coins():
    user_id = request.json['user_id']
    
    conn = sqlite3.connect('notcoin.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET coins = coins + 1 WHERE user_id=?', (user_id,))
    conn.commit()
    
    cursor.execute('SELECT coins FROM users WHERE user_id=?', (user_id,))
    coins = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({'status': 'success', 'coins': coins})


@app.route('/invite', methods=['POST'])
def invite():
    user_id = request.form['user_id']
    friend_username = request.form['friend_username']
    
    conn = sqlite3.connect('notcoin.db')
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

if __name__ == '__main__':
    app.run(debug=True)
