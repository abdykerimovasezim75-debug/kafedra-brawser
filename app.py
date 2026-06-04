# app.py
from flask import Flask, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

from auth_test import auth_test_bp
app.register_blueprint(auth_test_bp)

@app.route('/')
def index():
    return redirect(url_for('auth_test.login'))

if __name__ == '__main__':
    app.run(debug=True)