from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('radios.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to fetch radios based on the specified filters
def fetch_radios(current_user=False, available_radios=False):
    conn = get_db_connection()
    cursor = conn.cursor()

    if current_user and available_radios:
        # Display radios with a current user and available radios
        radios = cursor.execute('SELECT * FROM radios WHERE checked_out = 1').fetchall()
    elif current_user:
        # Display radios with a current user
        radios = cursor.execute('SELECT * FROM radios WHERE checked_out = 1').fetchall()
    elif available_radios:
        # Display available radios
        radios = cursor.execute('SELECT * FROM radios WHERE checked_out = 0').fetchall()
    else:
        # Display all radios
        radios = cursor.execute('SELECT * FROM radios').fetchall()

    conn.close()
    return radios

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Check if the parameters are provided in the request
    current_user = request.args.get('current_user') == 'true'
    available_radios = request.args.get('available_radios') == 'true'

    # Fetch radios based on the specified filters
    radios = fetch_radios(current_user=current_user, available_radios=available_radios)

    return render_template('dashboard.html', radios=radios, current_user=current_user, available_radios=available_radios)

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

@app.route('/add_radio', methods=['POST'])
def add_radio():
    radio_id = request.form['radio_id']
    model = request.form['model']
    serial_number = request.form['serial_number']
    conn = get_db_connection()
    conn.execute('INSERT INTO radios (id, model, serial_number, checked_out) VALUES (?, ?, ?, ?)',
                 (radio_id, model, serial_number, 0))  # Assuming checked_out is set to 0 for new radios
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
