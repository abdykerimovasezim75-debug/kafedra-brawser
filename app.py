from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from chatbot import get_response
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/teachers")
def teachers():
    return render_template("teachers.html")

@app.route("/subjects")
def subjects():
    return render_template("subjects.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/about-details")
def about_details():
    return render_template("about_details.html")

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    response = ""
    user_message = ""

    if request.method == "POST":
        user_message = request.form["message"]
        response = get_response(user_message)

    return render_template(
        "chatbot.html",
        response=response,
        user_message=user_message
    )

@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        if "user" not in session:
            return redirect(url_for("login"))

        text = request.form["review"]
        date = datetime.now().strftime("%d.%m.%Y")
        
        cursor.execute(
            "INSERT INTO reviews (username, text, date) VALUES (?, ?, ?)",
            (session["user"], text, date)
        )
        conn.commit()

    cursor.execute("SELECT * FROM reviews")
    all_reviews = cursor.fetchall()

    conn.close()

    return render_template("reviews.html", reviews=all_reviews)
 
@app.route("/like/<int:id>")
def like(id):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE reviews SET likes = likes + 1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("reviews"))

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM reviews WHERE id=?",
        (id,)
    )

    review = cursor.fetchone()

    if review and review[0] == session.get("user"):
        cursor.execute(
            "DELETE FROM reviews WHERE id=?",
            (id,)
        )
        conn.commit()

    conn.close()

    return redirect(url_for("reviews"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = username
            session["role"] = user[3]

            return redirect(url_for("home"))
        else:
            return "Неверный логин ❌"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = sqlite3.connect("database/database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )

        conn.commit()
        conn.close()

        session["user"] = username
        session["role"] = role

        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)