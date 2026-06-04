# database_mock.py
USERS_TABLE = {}
RESULTS_TABLE = {}

TESTS_TABLE = [
    {"id": "q1", "text": "Какой тип данных в Python является изменяемым (mutable)?", "variants": ["Список (list)", "Кортеж (tuple)", "Строка (str)"], "correct": "Список (list)"},
    {"id": "q2", "text": "Каким HTTP-методом обычно отправляют данные из формы регистрации на сервер?", "variants": ["GET", "POST", "DELETE"], "correct": "POST"},
    {"id": "q3", "text": "Какая SQL-команда используется для добавления новой записи в таблицу базы данных?", "variants": ["UPDATE", "SELECT", "INSERT INTO"], "correct": "INSERT INTO"},
    {"id": "q4", "text": "Что делает декоратор @app.route('/') во Flask?", "variants": ["Связывает URL-адрес с функцией на сервере", "Подключает базу данных", "Запускает HTML-анимацию"], "correct": "Связывает URL-адрес с функцией на сервере"},
    {"id": "q5", "text": "Какая команда в Git используется для отправки локальных коммитов в удаленный репозиторий GitHub?", "variants": ["git pull", "git push", "git commit"], "correct": "git push"},
    {"id": "q6", "text": "Зачем нужно хешировать пароли пользователей перед сохранением в базу данных?", "variants": ["Чтобы они занимали меньше места", "Для безопасности (при утечке данных)", "Для ускорения работы поиска"], "correct": "Для безопасности (при утечке данных)"},
    {"id": "q7", "text": "Что вернет выражение len({'a': 1, 'b': 2}) в Python?", "variants": ["1", "2", "4"], "correct": "2"},
    {"id": "q8", "text": "Какая SQL-функция используется для подсчета общего количества строк в таблице?", "variants": ["COUNT()", "SUM()", "AVG()"], "correct": "COUNT()"},
    {"id": "q9", "text": "Где выполняется JavaScript код, за который отвечает Frontend №3?", "variants": ["На сервере", "В базе данных", "В браузере пользователя"], "correct": "В браузере пользователя"},
    {"id": "q10", "text": "Какое расширение файла по умолчанию используется для SQLite базы данных?", "variants": [".db", ".py", ".html"], "correct": ".db"}
]

def add_user(username, password_hash, role="student"):
    USERS_TABLE[username] = {
        "password_hash": password_hash,
        "role": role
    }
    print(f"[БД LOG] Пользователь {username} зарегистрирован как [{role}].")
    return True

def get_user_password(username):
    user_data = USERS_TABLE.get(username)
    if user_data:
        return user_data["password_hash"]
    return None

def get_user_role(username):
    user_data = USERS_TABLE.get(username)
    return user_data["role"] if user_data else None

def get_test_questions():
    return TESTS_TABLE

def save_test_result(username, score):
    RESULTS_TABLE[username] = score
    print(f"[БД LOG] Результат {username}: {score} баллов сохранен.")
    return True