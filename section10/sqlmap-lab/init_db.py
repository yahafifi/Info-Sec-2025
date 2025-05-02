import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", [
    ("admin", "admin123"),
    ("maram", "marampass"),
    ("maryam", "maryampass")
])

conn.commit()
conn.close()
