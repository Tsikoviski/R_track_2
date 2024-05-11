from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('radios.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    radios = conn.execute('SELECT * FROM radios').fetchall()
    conn.close()
    return render_template('dashboard.html', radios=radios)

@app.route('/checkout', methods=['POST'])
def checkout():
    radio_id = request.form['id']
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    conn = get_db_connection()
    conn.execute('UPDATE radios SET checked_out=1, current_user_id=?, current_user_name=? WHERE id=?',
                 (user_id, user_name, radio_id))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/checkin', methods=['POST'])
def checkin():
    radio_id = request.form['id']
    conn = get_db_connection()
    conn.execute('UPDATE radios SET checked_out=0, current_user_id=NULL, current_user_name=NULL WHERE id=?', (radio_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
