import sqlite3
import datetime
import time

# Function to perform a checkout operation with retry logic
def checkout_radio(radio_id, user, employee_id):
    conn = sqlite3.connect('radios.db')
    cursor = conn.cursor()

    attempts = 0
    while attempts < 3:
        try:
            cursor.execute('''
                UPDATE radios
                SET checked_out = 1, 
                    current_user = ?, 
                    employee_id = ?, 
                    checkout_date = ?
                WHERE id = ?
            ''', (user, employee_id, datetime.datetime.now(), radio_id))
            conn.commit()
            break  # Exit the loop if the update is successful
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                # Database is locked, retry after a short delay
                attempts += 1
                time.sleep(0.1)  # Wait for 100 milliseconds
            else:
                raise  # Re-raise other operational errors

    conn.close()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('radios.db')
cursor = conn.cursor()

# Create or modify the radios table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS radios (
        id INTEGER PRIMARY KEY,
        type TEXT,
        model_number TEXT,
        current_user TEXT,
        employee_id TEXT,
        checked_out BOOLEAN NOT NULL DEFAULT 0,
        checkout_date TIMESTAMP
    )
''')

# Insert the specified radio records
radios_data = [
    ('Motorola', 'MDH02RDC9VA1AN', None, None, False, None),  # Adjust as needed
    ('Motorola', 'MDH02RDC9VA1BN', None, None, False, None),  # Adjust as needed
    ('Motorola', 'NDH56RDC9RA1AN', None, None, False, None)   # Adjust as needed
]

cursor.executemany('INSERT INTO radios (type, model_number, current_user, employee_id, checked_out, checkout_date) VALUES (?, ?, ?, ?, ?, ?)', radios_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
