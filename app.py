import os

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

app.secret_key = "12345"

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# максимум 2 MB
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024


@app.route("/")
def home():
    return "Сервер работает"


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/reviews", methods=["GET", "POST"])
def reviews():

    if request.method == "POST":

        photo = request.files["photo"]

        if photo:

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    photo.filename
                )
            )

            return "Фото загружено"

    return render_template("reviews.html")


if __name__ == "__main__":
    app.run(debug=True)