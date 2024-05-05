import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('radios.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create the radios table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS radios (
                    id INTEGER PRIMARY KEY,
                    type TEXT,
                    model_number TEXT,
                    current_user TEXT,
                    employee_id TEXT
                )''')

# Insert the specified radio records
radios_data = [
    ('Motorola', 'MDH02RDC9VA1AN', 'Emmanuel Arhin', '10162'),
    ('Motorola', 'MDH02RDC9VA1BN', 'Isaac Ackah', '12345'),
    ('Motorola', 'NDH56RDC9RA1AN', 'Frimpong Addo', 'FA3019')
]

cursor.executemany('INSERT INTO radios (type, model_number, current_user, employee_id) VALUES (?, ?, ?, ?)', radios_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

