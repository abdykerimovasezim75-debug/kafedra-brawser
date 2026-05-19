from database import get_db_connection


def add_review(username, comment):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reviews (username, comment) VALUES (?, ?)",
        (username, comment)
    )

    conn.commit()
    conn.close()


def get_reviews():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reviews")

    reviews = cursor.fetchall()

    conn.close()

    return reviews