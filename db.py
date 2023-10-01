import sqlite3

# Establish a connection to the SQLite database named 'pointsTracker.sqlite'
conn = sqlite3.connect("pointsTracker.sqlite")

cursor = conn.cursor()
sql_query =  """ CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    payer TEXT NOT NULL,
    points INTEGER NOT NULL,
    timestamp TEXT NOT NULL
);
 """
cursor.execute(sql_query)