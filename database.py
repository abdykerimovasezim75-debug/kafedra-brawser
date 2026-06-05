import sqlite3

DATABASE = "school.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            photo TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            level TEXT NOT NULL DEFAULT 'Бакалавриат'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            photo TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            text TEXT NOT NULL,
            rating INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def add_teacher(name, subject, photo=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO teachers (name, subject, photo) VALUES (?, ?, ?)",
        (name, subject, photo)
    )
    conn.commit()
    conn.close()


def get_all_teachers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    conn.close()
    return teachers


def add_subject(title, description=None, level="Бакалавриат"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subjects (title, description, level) VALUES (?, ?, ?)",
        (title, description, level)
    )
    conn.commit()
    conn.close()


def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    conn.close()
    return subjects


def add_news(title, content, date, photo=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO news (title, content, date, photo) VALUES (?, ?, ?, ?)",
        (title, content, date, photo)
    )
    conn.commit()
    conn.close()


def get_all_news():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news ORDER BY date DESC")
    all_news = cursor.fetchall()
    conn.close()
    return all_news


def add_review(author, text, rating, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reviews (author, text, rating, date) VALUES (?, ?, ?, ?)",
        (author, text, rating, date)
    )
    conn.commit()
    conn.close()


def get_all_reviews():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews ORDER BY date DESC")
    reviews = cursor.fetchall()
    conn.close()
    return reviews


if __name__ == "__main__":
    create_tables()

    add_teacher("Базарбаева Гулбарчин Долонбаевна", "к.фил.н., доцент каф КЛ")
    add_teacher("Абыкеев Капарбек Джолдошбекович", "к.т.н, доцент каф КЛ")
    add_teacher("Саякова Нуркыз Илимбековна", "Старший преподаватель")
    add_teacher("Жумалиева Гулира Эдилбековна", "зав.каф.КЛ, к.фил.н., профессор")
    add_teacher("Карабаева Сонунбубу Женишбековна", "к.фил.н., доцент кафедры КЛ")
    add_teacher("Бөрүкулова Гүлсада Шерматовна", "к.фил.н., доцент каф.КЛ")
    add_teacher("Убайдылдаева Нуркыз Акимжановна", "старший преподаватель")
    add_teacher("Укуева Клара Акиновна", "старший преподаватель")
    add_teacher("Жумабаева Айнагул Насирдиновна", "старший преподаватель")

    add_subject("Введение в объектно-ориентированное программирование", "Автор: Зыков С. В. (ИНТУИТ)", "Бакалавриат")
    add_subject("Статистический машинный перевод", "Автор: Филипп Кен (Кембридж)", "Бакалавриат")
    add_subject("Введение в информационный поиск", "Автор: Кристофер Д. Мэннинг", "Бакалавриат")
    add_subject("Основы языка Python", None, "Бакалавриат")
    add_subject("Основы теории и практики машинного перевода", "Автор: Филипп Кен (Кембридж)", "Бакалавриат")
    add_subject("Основы проектирования информационных систем с применением больших языковых моделей", None, "Бакалавриат")

    add_subject("Математические модели языка", None, "Магистратура")
    add_subject("Обработка естественного языка (NLP) и глубокое обучение", None, "Магистратура")
    add_subject("Автоматический перевод и кросс-языковые системы", None, "Магистратура")
    add_subject("Корпусная лингвистика и извлечение данных (Text Mining)", None, "Магистратура")
    add_subject("Семантический анализ и онтологии", None, "Магистратура")
    add_subject("Речевые технологии и синтез речи", None, "Магистратура")

    add_news(
        "Форум «Кыялымдагы Кыргызстан»",
        "10 ноября 2025 года состоялся форум «Кыялымдагы Кыргызстан», в котором приняли участие студенты кафедры «Компьютерной лингвистики» под руководством Нуркыз Илимбековны. Форум прошёл очень интересно и познавательно. Участники получили полезную информацию, обменялись опытом и узнали много нового о современных возможностях и развитии Кыргызстана. Также в рамках мероприятия был организован праздничный концерт, который подарил всем хорошее настроение и яркие эмоции. Для студентов это стало отличной возможностью проявить себя, расширить кругозор и получить мотивацию для дальнейшего развития.",
        "2025-11-10"
    )
    add_news(
        "Участие в финале хакатона Digital4Climate.kg",
        "10 февраля 2026 года студенты кафедры «Компьютерной лингвистики» Абдыкеримова Сезим и Искендерова Фатима приняли участие в финале хакатона Digital4Climate.kg. Во время хакатона участники получили ценный практический опыт, смогли применить свои знания на практике, поработать в команде и познакомиться с современными IT-решениями в сфере экологии и технологий. Участие в таком мероприятии стало важным шагом для профессионального развития студентов. Желаем им дальнейших успехов, новых достижений и побед!",
        "2026-02-10"
    )
    add_news(
        "Поход в театр имени Токтоболота Абдумомунова",
        "23 апреля 2026 года студенты кафедры «Компьютерной лингвистики» посетили Кыргызский национальный академический драматический театр имени Токтоболота Абдумомунова, где посмотрели спектакль «Энли-Кебек». Посещение театра подарило студентам яркие впечатления и позволило ближе познакомиться с культурным и духовным наследием. Студенты кафедры развиваются не только в сфере IT и современных технологий, но и уделяют внимание духовному, культурному и личностному развитию.",
        "2026-04-23"
    )

    add_review("Студент", "Именно здесь я поняла что IT — это моё направление. Очень нравится атмосфера на кафедре. Преподаватели всегда помогают и объясняют материал понятным языком. Благодаря проектам и хакатонам начала больше интересоваться IT и программированием.", 5, "2026-03-14")
    add_review("Студент", "Было бы хорошо, если бы на кафедре проводилось ещё больше практических занятий и мастер-классов. В целом обучение очень интересное, преподаватели отзывчивые, а атмосфера дружная и комфортная для студентов.", 4, "2026-04-02")
    add_review("Студент", "На кафедре дружная атмосфера и много возможностей для студентов. Особенно нравится участие в форумах, конкурсах и командных проектах. Учеба проходит интересно и современно.", 5, "2026-04-19")
    add_review("Студент", "В целом обучение на кафедре хорошее, но иногда не хватает более понятных объяснений на лекциях. Было бы лучше, если бы больше времени уделяли практике и разбору реальных примеров.", 4, "2026-05-11") 
