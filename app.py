from flask import Flask, render_template

app = Flask(__name__)

app.secret_key = "12345"


@app.route("/")
def home():
    return "Сервер работает"


@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)