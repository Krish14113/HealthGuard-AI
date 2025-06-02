import sqlite3

def create_connection():
    conn = sqlite3.connect('healthguard.db')  # Create or connect to the database file
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create table for storing user history
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        symptoms TEXT,
        heart_rate INTEGER,
        disease TEXT,
        confidence REAL
    )''')
    
    conn.commit()
    conn.close()

def save_to_db(symptoms, heart_rate, disease, confidence):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO history (symptoms, heart_rate, disease, confidence)
    VALUES (?, ?, ?, ?)''', (str(symptoms), heart_rate, disease, confidence))
    
    conn.commit()
    conn.close()

# Call create_table() once to initialize the database and table
#create_table()  # Uncomment this line the first time you run the code to set up the table
