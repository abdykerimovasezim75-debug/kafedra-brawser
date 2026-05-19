from flask import Flask
from auth import auth
from test_system import test_system

from flask import Flask
from auth import auth
from test_system import test_system

app = Flask(__name__)

app.secret_key = '12345'

app.register_blueprint(auth)
app.register_blueprint(test_system)

@app.route('/')
def home():
    return "Backend 3 работает"

if __name__ == '_main_':
    app.run(debug=True)
