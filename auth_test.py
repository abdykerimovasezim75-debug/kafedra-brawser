# auth_test.py
from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import database_mock  as database
import time

auth_test_bp = Blueprint('auth_test', __name__)

@auth_test_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if not email or not password or not role:
            return "Заполните все поля и выберите роль!", 400
            
        hashed_pw = generate_password_hash(password, method='scrypt')
        database.add_user(email, hashed_pw, role)
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
            user_role = database.get_user_role(email)
            
            # Разводка ролей: преподаватель идет в личный кабинет, студент на тест
            if user_role == 'teacher':
                return redirect(url_for('auth_test.teacher_dashboard'))
            else:
                session['answers'] = {}
                session['start_time'] = time.time()
                return redirect(url_for('auth_test.test_page', q_index=1))
            
        return "Неверная почта или пароль!", 401
        
    return render_template('login.html')

@auth_test_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_test.login'))

@auth_test_bp.route('/test/<int:q_index>', methods=['GET', 'POST'])
def test_page(q_index):
    if 'user' not in session:
        return "Сначала войдите! <a href='/login'>Войти</a>", 403

    questions = database.get_test_questions()
    total_q = len(questions)

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
            session['answers'] = answers

        action = request.form.get('action')
        if action == 'next':
            return redirect(url_for('auth_test.test_page', q_index=q_index + 1))
        elif action == 'prev':
            return redirect(url_for('auth_test.test_page', q_index=q_index - 1))
        elif action == 'submit':
            return redirect(url_for('auth_test.test_result'))

    saved_answer = session.get('answers', {}).get(current_question['id'], '')

    return render_template(
        'test.html', 
        q=current_question, 
        q_index=q_index, 
        total_q=total_q,
        saved_answer=saved_answer
    )

@auth_test_bp.route('/test/result')
def test_result():
    if 'user' not in session: 
        return redirect(url_for('auth_test.login'))

    end_time = time.time()
    start_time = session.get('start_time', end_time)
    duration_seconds = int(end_time - start_time)
    
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    time_str = f"{minutes:02d}:{seconds:02d}"

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

    percent = int((score / total_q) * 100) if total_q > 0 else 0
    
    if percent < 40:
        level = "Новичок"
    elif percent < 80:
        level = "Базовый"
    else:
        level = "Продвинутый"

    leaderboard_place = "3 из 27"
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

@auth_test_bp.route('/teacher/dashboard')
def teacher_dashboard():
    if 'user' not in session:
        return redirect(url_for('auth_test.login'))
        
    user_role = database.get_user_role(session['user'])
    if user_role != 'teacher':
        return "Доступ запрещен! Вы не преподаватель.", 403
        
    return f"""
        <body style="font-family: sans-serif; padding: 20px;">
            <h1>🎓 Панель преподавателя ИИТ КГТУ</h1>
            <p>Добро пожаловать, <strong>{session['user']}</strong>!</p>
            <hr>
            <h3>Панель управления в разработке (Здесь будут оценки от Backend №2)</h3>
            <br>
            <a href="/logout">Выйти из системы</a>
        </body>
    """