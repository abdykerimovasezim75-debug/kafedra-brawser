import sqlite3

conn = sqlite3.connect("database.db")
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

cursor.execute(
    "UPDATE users SET role='admin' WHERE username='admin'"
)

conn.commit()
conn.close()

print("Роль изменена")

# таблица reviews
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    text TEXT,
    date TEXT,
    likes INTEGER DEFAULT 0,
    photo TEXT
)
""")

# тестовый пользователь
cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    ("admin", "1234", "admin")
)

conn.commit()
conn.close()

print("База создана!")