# app.py
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import time

app = Flask(__name__)
# Постоянный секретный ключ, чтобы браузер не сбрасывал сессию при перезапуске сервера
app.secret_key = 'super_secret_key_for_iit_kstu_2026'

TEST_DURATION = 1200  # 20 минут на тест

# База данных в оперативной памяти
USERS_TABLE = {}
RESULTS_TABLE = {}

# Чистые тесты по Python, привязанные к старым системным ID для стабильности фронтенда
TESTS_DATA = {
    "nlp": [
        {"id": "q1", "text": "Какая функция в Python используется для вывода текста на экран?", "variants": ["input()", "print()", "output()", "def"], "correct": "print()"},
        {"id": "q2", "text": "Как правильно создать переменную и присвоить ей число 5?", "variants": ["x == 5", "variable 5 = x", "x = 5", "let x = 5"], "correct": "x = 5"},
        {"id": "q3", "text": "Каким знаком в Python обозначается операция умножения?", "variants": ["x", "*", "^", "/"], "correct": "*"},
        {"id": "q4", "text": "Какое ключевое слово используется для проверки условий (если...)?", "variants": ["for", "while", "if", "def"], "correct": "if"},
        {"id": "q5", "text": "Тип данных int отвечает за:", "variants": ["Целые числа", "Строки текста", "Дробные числа", "Списки"], "correct": "Целые числа"},
        {"id": "q6", "text": "Как обозначается однострочный комментарий в Python?", "variants": ["// комментарий", "/* комментарий */", "# комментарий", ""], "correct": "# комментарий"},
        {"id": "q7", "text": "Что делает оператор '%' в Python (например, 5 % 2)?", "variants": ["Считает проценты", "Делит без остатка", "Возводит в степень", "Находит остаток от деления"], "correct": "Находит остаток от деления"},
        {"id": "q8", "text": "Какая функция используется, чтобы узнать длину строки или количество элементов?", "variants": ["size()", "len()", "length()", "count()"], "correct": "len()"},
        {"id": "q9", "text": "Тип данных str отвечает за:", "variants": ["Логические значения", "Строки (текст)", "Списки элементов", "Дробные числа"], "correct": "Строки (текст)"},
        {"id": "q10", "text": "Что выведет код: print(2 + 3 * 2)?", "variants": ["10", "8", "7", "6"], "correct": "8"},
        {"id": "q11", "text": "Каким знаком обозначается строгое равенство в условиях Python?", "variants": ["=", "==", "===", "equals"], "correct": "=="},
        {"id": "q12", "text": "Что такое цикл 'for'?", "variants": ["Конструкция для повторения действий", "Название переменной", "Функция удаления", "Тип данных"], "correct": "Конструкция для повторения действий"},
        {"id": "q13", "text": "Какое ключевое слово используется для создания своей функции?", "variants": ["function", "def", "func", "create"], "correct": "def"},
        {"id": "q14", "text": "Какое расширение имеют файлы, написанные на Python?", "variants": [".py", ".txt", ".exe", ".html"], "correct": ".py"},
        {"id": "q15", "text": "Как переводится название типа данных bool (Boolean)?", "variants": ["Большой", "Текстовый", "Логический (Истина/Ложь)", "Дробный"], "correct": "Логический (Истина/Ложь)"}
    ],
    "translation": [
        {"id": "t1", "text": "Какое слово используется, чтобы вернуть результат работы из функции?", "variants": ["get", "give", "return", "exit"], "correct": "return"},
        {"id": "t2", "text": "Что будет, если запустить бесконечный цикл 'while True'?", "variants": ["Компьютер выключится", "Код будет выполняться бесконечно", "Выдаст ошибку синтаксиса", "Цикл выполнится 1 раз"], "correct": "Код будет выполняться бесконечно"},
        {"id": "t3", "text": "С помощью какой функции можно получить данные от пользователя через консоль?", "variants": ["print()", "input()", "read()", "scan()"], "correct": "input()"}
    ],
    "theory": [
        {"id": "th1", "text": "С какого индекса начинается отсчет элементов в списках Python?", "variants": ["С 1", "С 0", "С любого", "С -1"], "correct": "С 0"},
        {"id": "th2", "text": "Как правильно создать пустой список в Python?", "variants": ["my_list = []", "my_list = {}", "my_list = ()", "my_list = list(empty)"], "correct": "my_list = []"}
    ],
    "corpus": [
        {"id": "c1", "text": "Какую ошибку выдаст Python, если забыть поставить двоеточие ':' после if?", "variants": ["SyntaxError (Ошибка синтаксиса)", "NameError (Ошибка имени)", "TypeError (Ошибка типа)", "ZeroDivisionError"], "correct": "SyntaxError (Ошибка синтаксиса)"},
        {"id": "c2", "text": "Что играет важнейшую роль в Python для разделения блоков кода?", "variants": ["Точка с запятой ';'", "Фигурные скобки '{}'", "Отступы (пробелы или Tab)", "Кавычки"], "correct": "Отступы (пробелы или Tab)"}
    ]
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        if not email or not password or not role:
            return "Заполните все поля!", 400
        USERS_TABLE[email] = {"password_hash": generate_password_hash(password, method='scrypt'), "role": role}
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = USERS_TABLE.get(email)
        if user_data and check_password_hash(user_data["password_hash"], password):
            session['user'] = email
            if user_data["role"] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            return redirect(url_for('categories'))
        return "Неверная почта или пароль!", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/categories')
def categories():
    if 'user' not in session: 
        return redirect(url_for('login'))
    return render_template('categories.html')

@app.route('/test/preview/<category_id>')
def test_preview(category_id):
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    meta = {
        "nlp": {"title": "🐍 Основы Python", "desc": "Проверка базового синтаксиса, переменных и простых вычислений.", "count": 15},
        "translation": {"title": "⚙️ Функции и циклы", "desc": "Разбор работы циклов for/while и создания собственных функций def.", "count": 3},
        "theory": {"title": "📦 Списки и словари", "desc": "Изучение базовых структур данных в Python, индексов и встроенных методов.", "count": 2},
        "corpus": {"title": "❌ Ошибки в коде", "desc": "Поиск синтаксических ошибок, исключений и понимание роли отступов.", "count": 2}
    }
    current_meta = meta.get(category_id, {"title": "Тест по Python", "desc": "Тестирование знаний", "count": 10})
    return render_template('preview.html', category_id=category_id, meta=current_meta)

@app.route('/test/start/<category_id>')
def start_test_session(category_id):
    if 'user' not in session: 
        return redirect(url_for('login'))
    session['current_category'] = category_id
    session['answers'] = {}
    session['start_time'] = time.time()
    return redirect(url_for('test_page', q_index=1))

@app.route('/test/<int:q_index>', methods=['GET', 'POST'])
def test_page(q_index):
    if 'user' not in session: 
        return redirect(url_for('login'))
    if 'start_time' not in session: 
        return redirect(url_for('categories'))

    elapsed_time = time.time() - session['start_time']
    time_left = int(TEST_DURATION - elapsed_time)
    if time_left <= 0:
        return redirect(url_for('test_result'))

    category_id = session.get('current_category', 'nlp')
    questions = TESTS_DATA.get(category_id, TESTS_DATA["nlp"])
    total_q = len(questions)

    if q_index < 1 or q_index > total_q:
        return redirect(url_for('test_page', q_index=1))

    current_question = questions[q_index - 1]

    if request.method == 'POST':
        selected_variant = request.form.get('variant')
        if selected_variant:
            answers = session.get('answers', {})
            answers[current_question['id']] = selected_variant
            session['answers'] = answers

        action = request.form.get('action')
        if action == 'next':
            return redirect(url_for('test_page', q_index=q_index + 1))
        elif action == 'prev':
            return redirect(url_for('test_page', q_index=q_index - 1))
        elif action == 'submit':
            return redirect(url_for('test_result'))

    saved_answer = session.get('answers', {}).get(current_question['id'], '')
    timer_string = f"{max(0, time_left // 60):02d}:{max(0, time_left % 60):02d}"

    return render_template(
        'test.html', 
        q=current_question, q_index=q_index, total_q=total_q,
        saved_answer=saved_answer, timer_string=timer_string, time_left_seconds=time_left
    )

@app.route('/test/result')
def test_result():
    if 'user' not in session or 'start_time' not in session: 
        return redirect(url_for('login'))

    duration = min(int(time.time() - session['start_time']), TEST_DURATION)
    time_str = f"{duration // 60:02d}:{duration % 60:02d}"

    category_id = session.get('current_category', 'nlp')
    questions = TESTS_DATA.get(category_id, TESTS_DATA["nlp"])
    user_answers = session.get('answers', {})
    
    score = sum(1 for q in questions if user_answers.get(q['id']) == q['correct'])
    total_q = len(questions)
    percent = int((score / total_q) * 100) if total_q > 0 else 0
    
    report = [{"text": q['text'], "user_ans": user_answers.get(q['id'], "Не отвечено"), "correct_ans": q['correct'], "is_correct": user_answers.get(q['id']) == q['correct']} for q in questions]

    RESULTS_TABLE[session['user']] = score

    return render_template(
        'result.html', score=score, total=total_q, percent=percent,
        time_spent=time_str, place="3 из 27", level="Базовый" if percent >= 40 else "Новичок", report=report
    )

@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'user' not in session: 
        return redirect(url_for('login'))
    return "<h1>🎓 Панель преподавателя ИИТ КГТУ</h1><br><a href='/logout'>Выход</a>"

if __name__ == '__main__':
    app.run(debug=True)