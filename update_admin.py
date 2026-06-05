import sqlite3


conn = sqlite3.connect("database/databasefama.db")
cursor = conn.cursor()


cursor.execute("SELECT * FROM users")


for user in cursor.fetchall():
    print(user)


conn.close()
