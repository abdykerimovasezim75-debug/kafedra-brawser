from flask import Flask, render_template

app = Flask(__name__)

app.secret_key = "12345"


@app.route("/")
def home():
    return "Сервер работает"


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


if __name__ == "__main__":
    app.run(debug=True)
