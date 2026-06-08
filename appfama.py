from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from chatbot import get_response
from datetime import datetime
import os
from PIL import Image
from werkzeug.utils import secure_filename
from database import get_all_teachers, get_all_subjects, get_all_news



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
    teachers = get_all_teachers()
    return render_template("teachers.html", teachers=teachers)

@app.route("/subjects")
def subjects():
    subjects = get_all_subjects()
    return render_template("subjects.html", subjects=subjects)

@app.route("/news")
def news():
    news = get_all_news()
    return render_template("news.html", news=news)

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/about-details")
def about_details():
    return render_template("about_details.html")

@app.route("/subject/math_models")
def math_models():
    return render_template("math_models.html")

@app.route("/subject/oop")
def oop():
    return render_template("oop.html")

@app.route("/subject/statistical_mt")
def statistical_mt():
    return render_template("statistical_mt.html")

@app.route("/subject/information_retrieval")
def information_retrieval():
    return render_template("information_retrieval.html")

@app.route("/subject/python_basics")
def python_basics():
    return render_template("python_basics.html")

@app.route("/subject/translation_theory")
def translation_theory():
    return render_template("translation_theory.html")

@app.route("/subject/llm_system_design")
def llm_system_design():
    return render_template("llm_system_design.html")

@app.route("/subject/nlp_deep_learning")
def nlp_deep_learning():
    return render_template("nlp.html")

@app.route("/subject/machine_translation")
def machine_translation():
    return render_template("machine_translation.html")

@app.route("/subject/text_mining")
def text_mining():
    return render_template("text_mining.html")

@app.route("/subject/semantic_analysis")
def semantic_analysis():
    return render_template("semantic_analysis.html")

@app.route("/subject/speech_technology")
def speech_technology():
    return render_template("speech_technology.html")

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
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/all_reviews")
def all_reviews():

    conn = sqlite3.connect("database/databasefama.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()

    conn.close()

    return render_template("all_reviews.html", reviews=reviews)

@app.route("/reviews", methods=["GET", "POST"])
def reviews():

    conn = sqlite3.connect("database/databasefama.db")
    cursor = conn.cursor()

    if request.method == "POST":

        if "user" not in session:
            return redirect(url_for("login"))

        text = request.form["review"]
        date = datetime.now().strftime("%d.%m.%Y")

        photo = request.files["photo"]

        filename = None

        if photo and photo.filename:

            filename = secure_filename(photo.filename)

            path = os.path.join("static/uploads", filename)

            photo.save(path)

            img = Image.open(path)
            img.thumbnail((800, 800))
            img.save(path, quality=65)

        cursor.execute(
            """
            INSERT INTO reviews (username, text, date, photo)
            VALUES (?, ?, ?, ?)
            """,
            (session["user"], text, date, filename)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("all_reviews"))

    cursor.execute("SELECT * FROM reviews")
    all_reviews = cursor.fetchall()

    conn.close()

    return render_template(
        "reviews.html",
        reviews=all_reviews
    )
 
@app.route("/like/<int:id>")
def like(id):
    conn = sqlite3.connect("database/databasefama.db")
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

    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database/databasefama.db")
    cursor = conn.cursor()

    if session.get("role") == "admin":
        cursor.execute(
            "DELETE FROM reviews WHERE id=?",
            (id,)
        )
    else:
        cursor.execute(
            "DELETE FROM reviews WHERE id=? AND username=?",
            (id, session["user"])
        )

    conn.commit()
    conn.close()

    return redirect(url_for("reviews"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/databasefama.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()

        print("username =", repr(username))
        print("user =", user)

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

        conn = sqlite3.connect("database/databasefama.db")
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
