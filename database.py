import sqlite3

conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

# таблица users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# таблица reviews
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    text TEXT,
    date TEXT,
    likes INTEGER DEFAULT 0
)
""")

# тестовый пользователь
cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("admin", "1234",  "teacher")
)

conn.commit()
conn.close()

print("База создана!")