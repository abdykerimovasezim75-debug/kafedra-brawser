# app.py
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import time

app = Flask(__name__)
# Постоянный секретный ключ для фиксации сессий в браузере
app.secret_key = 'iit_kstu_computer_linguistics_2026'

TEST_DURATION = 1200  # 20 минут (1200 секунд)

# База данных пользователей и результатов в оперативной памяти (In-Memory)
USERS_TABLE = {}
RESULTS_TABLE = {}

# Реальные данные тестов со страниц image_12.png, image_13.png и image_14.png
TESTS_DATA = {
    "theoretical": [ # Теоретическая лингвистика
        {"id": "tl1", "text": "Какой раздел лингвистики изучает звуковой строй языка?", "variants": ["Семантика", "Фонетика", "Синтаксис", "Морфология"], "correct": "Фонетика"},
        {"id": "tl2", "text": "Что является минимальной значимой единицей языка?", "variants": ["Фонема", "Морфема", "Слово", "Слог"], "correct": "Морфема"}
    ],
    "nlp": [ # Обработка текстов (Основы НЛП)
        {"id": "q1", "text": "Что из перечисленного относится к задачам обработки естественного языка?", "variants": ["Классификация изображений", "Распознавание речи", "Синтаксический анализ текста", "Обработка табличных данных"], "correct": "Синтаксический анализ текста"},
        {"id": "q2", "text": "Как называется процесс приведения слова к его неизменяемой базовой форме (лемме)?", "variants": ["Токенизация", "Лемматизация", "Стемминг", "Парсинг"], "correct": "Лемматизация"},
        {"id": "q3", "text": "Что такое токенизация в задачах NLP?", "variants": ["Удаление знаков препинания", "Разделение текста на отдельные слова или символы", "Перевод текста на другой язык", "Поиск стоп-слов"], "correct": "Разделение текста на отдельные слова или символы"}
    ],
    "translation": [ # Машинный перевод
        {"id": "t1", "text": "Какая архитектура нейросетей совершила революцию в машинном переводе?", "variants": ["CNN (Разверточные сети)", "Transformer (Трансформеры)", "Марковские модели", "Линейная регрессия"], "correct": "Transformer (Трансформеры)"},
        {"id": "t2", "text": "Что оценивает метрика BLEU в машинном переводе?", "variants": ["Скорость перевода", "Качество машинного перевода по сравнению с человеческим", "Размер словаря", "Количество грамматических ошибок"], "correct": "Качество машинного перевода по сравнению с человеческим"}
    ],
    "corpus": [ # Корпусная лингвистика
        {"id": "c1", "text": "Что такое лингвистический корпус?", "variants": ["Учебник по языкознанию", "Собрание текстов, подобранных и размеченных по определенным правилам", "Словарь иностранных слов", "Здание филологического факультета"], "correct": "Собрание текстов, подобранных и размеченных по определенным правилам"},
        {"id": "c2", "text": "Как называется автоматическое добавление лингвистической информации в корпус?", "variants": ["Разметка (аннотация)", "Индексация", "Фильтрация", "Сортировка"], "correct": "Разметка (аннотация)"}
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
        "theoretical": {"title": "Теоретическая лингвистика", "desc": "Проверьте знания в области фонетики, морфологии и синтаксиса.", "count": 2, "time": 10},
        "nlp": {"title": "Основы НЛП", "desc": "Проверьте знания базовых понятий обработки естественного языка.", "count": 15, "time": 20},
        "translation": {"title": "Машинный перевод", "desc": "Основные методы, подходы и метрики в машинном переводе.", "count": 18, "time": 25},
        "corpus": {"title": "Корпусная лингвистика", "desc": "Создание, разметка и анализ лингвистических корпусов данных.", "count": 4, "time": 15}
    }
    current_meta = meta.get(category_id, {"title": "Тест по лингвистике", "desc": "Тестирование знаний", "count": 10, "time": 20})
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
            if q_index < total_q:
                return redirect(url_for('test_page', q_index=q_index + 1))
            else:
                return redirect(url_for('test_result'))
        elif action == 'prev':
            return redirect(url_for('test_page', q_index=q_index - 1))
        elif action == 'submit':
            return redirect(url_for('test_result'))

    saved_answer = session.get('answers', {}).get(current_question['id'], '')
    timer_string = f"{max(0, time_left // 60):02d}:{max(0, time_left % 60):02d}"

    return render_template(
        'test.html', 
        category_title=category_id,
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
        time_spent=time_str, place="1 из 15", level="Продвинутый" if percent >= 75 else "Базовый", report=report
    )

@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'user' not in session: 
        return redirect(url_for('login'))
    return "<h1>🎓 Панель преподавателя кафедры Компьютерной лингвистики</h1><br><a href='/logout'>Выход</a>"

if __name__ == '__main__':
    app.run(debug=True)