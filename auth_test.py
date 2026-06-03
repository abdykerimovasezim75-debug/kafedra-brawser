# auth_test.py (ФИНАЛЬНАЯ ПОЛНАЯ ВЕРСИЯ)
from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import database_mock as database
import time  # Для подсчета времени прохождения теста

auth_test_bp = Blueprint('auth_test', __name__)

# --- 1. АУТЕНТИФИКАЦИЯ (ПО ПОЧТЕ ИЗ FIGMA) ---
@auth_test_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')  # Принимаем email вместо username
        password = request.form.get('password')
        
        if not email or not password:
            return "Заполните все поля!", 400
            
        hashed_pw = generate_password_hash(password, method='scrypt')
        database.add_user(email, hashed_pw)
        return redirect(url_for('auth_test.login'))
        
    return render_template('login.html')

@auth_test_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_hash = database.get_user_password(email)
        
        if user_hash and check_password_hash(user_hash, password):
            session['user'] = email
            session['answers'] = {}        # Очищаем старые ответы перед новым тестом
            session['start_time'] = time.time()  # Включаем секундомер
            return redirect(url_for('auth_test.test_page', q_index=1))
            
        return "Неверная почта или пароль!", 401
        
    return render_template('login.html')

@auth_test_bp.route('/logout')
def logout():
    session.clear()  # Полностью очищаем сессию при выходе
    return redirect(url_for('auth_test.login'))


# --- 2. ПОСТРАНИЧНЫЙ ТЕСТ (1 ВОПРОС НА СТРАНИЦУ) ---
@auth_test_bp.route('/test/<int:q_index>', methods=['GET', 'POST'])
def test_page(q_index):
    if 'user' not in session:
        return "Сначала войдите! <a href='/login'>Войти</a>", 403

    questions = database.get_test_questions()
    total_q = len(questions)

    # Защита от выхода за пределы (если ввели /test/99)
    if q_index < 1 or q_index > total_q:
        return redirect(url_for('auth_test.test_page', q_index=1))

    current_question = questions[q_index - 1]

    if request.method == 'POST':
        selected_variant = request.form.get('variant')
        if selected_variant:
            if 'answers' not in session: 
                session['answers'] = {}
            answers = session['answers']
            answers[current_question['id']] = selected_variant
            session['answers'] = answers  # Сохраняем выбор в сессию

        # Логика кнопок перемещения
        action = request.form.get('action')
        if action == 'next':
            return redirect(url_for('auth_test.test_page', q_index=q_index + 1))
        elif action == 'prev':
            return redirect(url_for('auth_test.test_page', q_index=q_index - 1))
        elif action == 'submit':
            return redirect(url_for('auth_test.test_result'))

    # Вытаскиваем ответ, если ученик тут уже был, чтобы галочка не слетала
    saved_answer = session.get('answers', {}).get(current_question['id'], '')

    return render_template(
        'test.html', 
        q=current_question, 
        q_index=q_index, 
        total_q=total_q,
        saved_answer=saved_answer
    )


# --- 3. СТРАНИЦА РЕЗУЛЬТАТОВ И РАЗБОРА ОШИБОК (ДЛЯ FIGMA) ---
@auth_test_bp.route('/test/result')
def test_result():
    if 'user' not in session: 
        return redirect(url_for('auth_test.login'))

    # Подсчет времени
    end_time = time.time()
    start_time = session.get('start_time', end_time)
    duration_seconds = int(end_time - start_time)
    
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    time_str = f"{minutes:02d}:{seconds:02d}"  # Формат 18:32 как на макете

    # Проверка ответов
    questions = database.get_test_questions()
    total_q = len(questions)
    user_answers = session.get('answers', {})
    
    score = 0
    report = []

    for q in questions:
        u_ans = user_answers.get(q['id'], "Не отвечено")
        is_correct = (u_ans == q['correct'])
        if is_correct: 
            score += 1

        report.append({
            "text": q['text'],
            "user_ans": u_ans,
            "correct_ans": q['correct'],
            "is_correct": is_correct
        })

    # Расчет процентов и уровня для Figma
    percent = int((score / total_q) * 100) if total_q > 0 else 0
    
    if percent < 40:
        level = "Новичок"
    elif percent < 80:
        level = "Базовый"
    else:
        level = "Продвинутый"

    # Заглушка для места в рейтинге
    leaderboard_place = "3 из 27"

    # Сохраняем в бэкап базы данных
    database.save_test_result(session['user'], score)

    return render_template(
        'result.html', 
        score=score, 
        total=total_q, 
        percent=percent,
        time_spent=time_str, 
        place=leaderboard_place,
        level=level,
        report=report
    )