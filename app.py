import time
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'kstu_secret_2026'

USERS = {}

QUESTIONS = {
    "theory": [
        {"id": 1, "text": "Какой раздел изучает звуковой строй языка?", "variants": ["Фонетика", "Морфология", "Синтаксис", "Семантика"], "correct": "Фонетика"},
        {"id": 2, "text": "Минимальная значимая единица языка — это...", "variants": ["Морфема", "Фонема", "Слово", "Предложение"], "correct": "Морфема"},
        {"id": 3, "text": "Какая наука изучает свойства знаков и знаковых систем?", "variants": ["Семиотика", "Этимология", "Лексикология", "Топонимика"], "correct": "Семиотика"},
        {"id": 4, "text": "Раздел лингвистики, изучающий структуру предложений?", "variants": ["Синтаксис", "Морфология", "Орфография", "Пунктуация"], "correct": "Синтаксис"},
        {"id": 5, "text": "Что именно изучает лексическая семантика?", "variants": ["Значения слов", "Звуки речи", "Буквы и графику", "Знаки препинания"], "correct": "Значения слов"},
        {"id": 6, "text": "Кто является автором знаменитого «Курса общей лингвистики»?", "variants": ["Фердинанд де Соссюр", "Ноам Хомский", "Роман Якобсон", "Вильгельм фон Гумбольдт"], "correct": "Фердинанд де Соссюр"},
        {"id": 7, "text": "Что изучает раздел акцентологии?", "variants": ["Особенности ударения", "Речевые звуки", "Слогоделение", "Интонационные контуры"], "correct": "Особенности ударения"},
        {"id": 8, "text": "Как называется наука о происхождении слов?", "variants": ["Этимология", "Стилистика", "Риторика", "Морфология"], "correct": "Этимология"},
        {"id": 9, "text": "Какое свойство языкового знака указывает на отсутствие естественной связи между формой и смыслом?", "variants": ["Произвольность", "Зависимость", "Случайность", "Линейность"], "correct": "Произвольность"},
        {"id": 10, "text": "Как называют абстрактную единицу звукового уровня языка?", "variants": ["Фонема", "Аллофон", "Морф", "Графема"], "correct": "Фонема"},
        {"id": 11, "text": "Какой тип связи возникает между подлежащим и сказуемым?", "variants": ["Согласование", "Управление", "Примыкание", "Координация"], "correct": "Координация"},
        {"id": 12, "text": "Изучением территориальных разновидностей языка занимается...", "variants": ["Диалектология", "Фонетика", "Лексикология", "Грамматика"], "correct": "Диалектология"},
        {"id": 13, "text": "Слова одной части речи, одинаковые по написанию, но разные по значению?", "variants": ["Омонимы", "Синонимы", "Антонимы", "Паронимы"], "correct": "Омонимы"},
        {"id": 14, "text": "Как называется устойчивое семантически неделимое сочетание слов?", "variants": ["Фразеологизм", "Свободное словосочетание", "Простое предложение", "Сложный текст"], "correct": "Фразеологизм"},
        {"id": 15, "text": "Раздел языкознания, фиксирующий правила правописания слов?", "variants": ["Орфография", "Фонетика", "Стилистика", "Синтаксис"], "correct": "Орфография"}
    ],
    "nlp": [
        {"id": 1, "text": "Что означает аббревиатура NLP?", "variants": ["Natural Language Processing", "Network Layer Protocol", "Node Language Parser", "Numerical Linear Program"], "correct": "Natural Language Processing"},
        {"id": 2, "text": "Что такое токенизация?", "variants": ["Разбиение текста на отдельные слова или символы", "Перевод текста на другой язык", "Сжатие текстовых данных", "Поиск ключевых слов в документе"], "correct": "Разбиение текста на отдельные слова или символы"},
        {"id": 3, "text": "Процесс приведения слова к его базовой, словарной форме называют...", "variants": ["Лемматизация", "Стемминг", "Токенизация", "Парсинг"], "correct": "Лемматизация"},
        {"id": 4, "text": "Как в NLP называют часто встречающиеся слова, не несущие уникального смысла (предлоги, союзы)?", "variants": ["Стоп-слова", "Ключевые термины", "Системные команды", "Служебные существительные"], "correct": "Стоп-слова"},
        {"id": 5, "text": "Грубый эвристический процесс отсечения окончаний слова называют...", "variants": ["Стемминг", "Лемматизация", "Парсинг", "Токенизация"], "correct": "Стемминг"},
        {"id": 6, "text": "Какая статистическая модель оценивает важность слова для конкретного документа в коллекции?", "variants": ["TF-IDF", "Bag-of-Words", "One-hot encoding", "Word2Vec"], "correct": "TF-IDF"},
        {"id": 7, "text": "Что означает задача NER в обработке текстов?", "variants": ["Распознавание именованных сущностей", "Машинный перевод", "Генерация аннотаций", "Определение частей речи"], "correct": "Распознавание именованных сущностей"},
        {"id": 8, "text": "Какая известная предобученная языковая модель была разработана Google в 2018 году?", "variants": ["BERT", "GPT", "RNN", "ResNet"], "correct": "BERT"},
        {"id": 9, "text": "Как называется последовательность, состоящая ровно из двух подряд идущих токенов?", "variants": ["Биграмма", "Униграмма", "Триграмма", "Тетраграмма"], "correct": "Биграмма"},
        {"id": 10, "text": "Как называется плотное векторное представление слова, отражающее его семантику?", "variants": ["Эмбеддинг", "Лемма", "Токен", "Хэш"], "correct": "Эмбеддинг"},
        {"id": 11, "text": "Как называется задача определения эмоциональной окраски текста?", "variants": ["Sentiment Analysis", "POS Tagging", "Text Summarization", "Dependency Parsing"], "correct": "Sentiment Analysis"},
        {"id": 12, "text": "Какая метрика используется для оценки качества работы языковых моделей?", "variants": ["Перплексия", "Метрика Евклида", "Косинусное расстояние", "Инвариант"], "correct": "Перплексия"},
        {"id": 13, "text": "Какая архитектура нейросетей, основанная на механизме Self-Attention, совершила революцию в NLP?", "variants": ["Transformer", "LSTM", "CNN", "MLP"], "correct": "Transformer"},
        {"id": 14, "text": "Что представляет собой n-грамма?", "variants": ["Последовательность из n элементов", "Вес токена в документе", "Символьный маркер", "Длина предложения в символах"], "correct": "Последовательность из n элементов"},
        {"id": 15, "text": "Какая библиотека Python является классическим инструментом для академических задач NLP?", "variants": ["NLTK", "OpenCV", "PyQt5", "Django"], "correct": "NLTK"}
    ],
    "translation": [
        {"id": 1, "text": "Как расшифровывается аббревиатура NMT?", "variants": ["Neural Machine Translation", "Native Modern Text", "Network Matrix Transfer", "Normal Model Token"], "correct": "Neural Machine Translation"},
        {"id": 2, "text": "Какая метрика является стандартной для автоматической оценки качества машинного перевода?", "variants": ["BLEU", "Accuracy", "F1-Score", "Recall"], "correct": "BLEU"},
        {"id": 3, "text": "Как называется подход к переводу, основанный на строгих лингвистических правилах и словарях?", "variants": ["RBMT", "SMT", "NMT", "LLM-based"], "correct": "RBMT"},
        {"id": 4, "text": "Концепция искусственного языка-посредника, хранящего чистый смысл предложений при переводе?", "variants": ["Интерлингва", "Лемма", "Стемм", "Метаязык"], "correct": "Интерлингва"},
        {"id": 5, "text": "Какой алгоритм часто применяется для кодирования слов в виде субтокенов (подслов) в NMT?", "variants": ["BPE (Byte Pair Encoding)", "TF-IDF", "Word2Vec", "Levenshtein Distance"], "correct": "BPE (Byte Pair Encoding)"},
        {"id": 6, "text": "Каку роль выполняет компонент Encoder в архитектуре машинного перевода?", "variants": ["Формирует векторное представление исходного текста", "Генерирует слова на целевом языке", "Удаляет знаки препинания", "Считает метрику качества"], "correct": "Формирует векторное представление исходного текста"},
        {"id": 7, "text": "Какую роль выполняет компонент Decoder в архитектуре машинного перевода?", "variants": ["Пошагово генерирует текст на целевом языке", "Анализирует синтаксис оригинала", "Очищает стоп-слова", "Выполняет токенизацию текста"], "correct": "Пошагово генерирует текст на целевом языке"},
        {"id": 8, "text": "Как называется проблема, когда в исходном тексте встречаются слова, отсутствующие в словаре модели?", "variants": ["OOV (Out-Of-Vocabulary)", "Полисемия", "Градиентный взрыв", "Переобучение"], "correct": "OOV (Out-Of-Vocabulary)"},
        {"id": 9, "text": "Как в машинном переводе называют процесс установления пословного соответствия между оригиналом и переводом?", "variants": ["Alignment (Выравнивание)", "Parsing", "Tokenization", "Stemming"], "correct": "Alignment (Выравнивание)"},
        {"id": 10, "text": "Способность модели переводить между языковыми парами, для которых не было явных обучающих примеров?", "variants": ["Zero-shot translation", "Supervised learning", "Rule-based translation", "Fine-tuning"], "correct": "Zero-shot translation"},
        {"id": 11, "text": "Что вызывает наибольшую сложность при автоматическом переводе многозначных слов?", "variants": ["Лексическая полисемия", "Длина предложения", "Шрифт текста", "Регистр букв"], "correct": "Лексическая полисемия"},
        {"id": 12, "text": "Как называется задача автоматического распознавания того, на каком языке написан входной текст?", "variants": ["LID (Language Identification)", "NER", "POS Tagging", "BPE"], "correct": "LID (Language Identification)"},
        {"id": 13, "text": "Изменение порядка слов при переводе для соответствия грамматике целевого языка — это...", "variants": ["Реструктуризация", "Лемматизация", "Стемминг", "Нормализация"], "correct": "Реструктуризация"},
        {"id": 14, "text": "Какая метрика оценки перевода учитывает синонимы и словоформы, в отличие от базового BLEU?", "variants": ["METEOR", "ROUGE", "MSE", "Perplexity"], "correct": "METEOR"},
        {"id": 15, "text": "Какое направление доминировало в машинном переводе до массового прихода глубоких нейросетей?", "variants": ["SMT (Статистический перевод)", "RBMT", "Аналоговый перевод", "Прямой пословный перевод"], "correct": "SMT (Статистический перевод)"}
    ],
    "corpus": [
        {"id": 1, "text": "Что такое лингвистический корпус?", "variants": ["Упорядоченное и размеченное собрание текстов", "Большой академический словарь", "Здание филологического факультета", "Учебник по грамматике"], "correct": "Упорядоченное и размеченное собрание текстов"},
        {"id": 2, "text": "Что представляет собой аннотация (разметка) корпуса?", "variants": ["Приписывание текстам и словам специальных лингвистических тегов", "Сортировка файлов по алфавиту", "Исправление орфографических ошибок", "Перевод текстов на иностранный язык"], "correct": "Приписывание текстам и словам специальных лингвистических тегов"},
        {"id": 3, "text": "Как называется корпус, состоящий из оригинальных текстов и их точных переводов на другие языки?", "variants": ["Параллельный корпус", "Сравнительный корпус", "Диахронический корпус", "Устный корпус"], "correct": "Параллельный корпус"},
        {"id": 4, "text": "Инструмент, показывающий все вхождения искомого слова вместе с его ближайшим текстовым контекстом?", "variants": ["Конкорданс", "Парсер", "Токенизатор", "Лемматизатор"], "correct": "Конкорданс"},
        {"id": 5, "text": "Как называется автоматическая разметка частей речи в корпусе?", "variants": ["POS-tagging", "Syntactic parsing", "NER", "Semantic analysis"], "correct": "POS-tagging"},
        {"id": 6, "text": "Какой эмпирический закон утверждает, что частота встречаемости слова обратно пропорциональна его рангу?", "variants": ["Закон Ципфа", "Закон Хеппа", "Закон Мандельброта", "Закон Парето"], "correct": "Закон Ципфа"},
        {"id": 7, "text": "Как называют корпус, фиксирующий срез языка в строго определенный, узкий промежуток времени?", "variants": ["Синхронный корпус", "Диахронный корпус", "Параллельный корпус", "Динамический корпус"], "correct": "Синхронный корпус"},
        {"id": 8, "text": "Как называют корпус, созданный для отслеживания исторических изменений языка на протяжении эпох?", "variants": ["Диахронный корпус", "Синхронный корпус", "Моноязычный корпус", "Специализированный корпус"], "correct": "Диахронный корпус"},
        {"id": 9, "text": "Что означает аббревиатура KWIC в корпусных поисковых системах?", "variants": ["Key Word In Context", "Key Word In Corpus", "Known Word In Content", "Keywords Index Construction"], "correct": "Key Word In Context"},
        {"id": 10, "text": "Какое свойство корпуса гарантирует, что он адекватно отражает реальное состояние исследуемого языка?", "variants": ["Репрезентативность", "Объем в гигабайтах", "Анонимность авторов", "Количество языков"], "correct": "Репрезентативность"},
        {"id": 11, "text": "Устойчивые словосочетания, обнаруживаемые в корпусе с помощью статистических тестов?", "variants": ["Коллокации", "Омонимы", "Синонимы", "Денотаты"], "correct": "Коллокации"},
        {"id": 12, "text": "Как называется упорядоченный список всех лемм корпуса с указанием абсолютной частоты их встречаемости?", "variants": ["Частотный словарь", "Тезаурус", "Алфавитный указатель", "Сводная таблица"], "correct": "Частотный словарь"},
        {"id": 13, "text": "Какая разметка отображает синтаксические связи между словами в виде деревьев зависимостей?", "variants": ["Синтаксическая аннотация", "Морфологический теггинг", "Семантическое картирование", "Прагматическая разметка"], "correct": "Синтаксическая аннотация"},
        {"id": 14, "text": "Специализированное программное обеспечение для управления, поиска и анализа данных в корпусах?", "variants": ["Корпус-менеджер", "Браузер", "Компилятор", "СУБД общего назначения"], "correct": "Корпус-менеджер"},
        {"id": 15, "text": "Информация об авторе, дате создания текста, его жанре и стиле называется...", "variants": ["Метаданные", "Стеммы", "Контекст", "Параметры разметки"], "correct": "Метаданные"}
    ],
    "python": [
        {"id": 1, "text": "Каким синтаксисом в Python можно инициализировать пустой список?", "variants": ["[]", "()", "{}", "set()"], "correct": "[]"},
        {"id": 2, "text": "Какая встроенная функция используется для вывода информации на стандартное устройство вывода?", "variants": ["print()", "show()", "log()", "echo()"], "correct": "print()"},
        {"id": 3, "text": "Какое ключевое слово зарезервировано в Python для объявления пользовательской функции?", "variants": ["def", "function", "func", "lambda"], "correct": "def"},
        {"id": 4, "text": "С помощью каких скобок создается структура данных 'словарь' (dict) в Python?", "variants": ["Фигурные {}", "Квадратные []", "Круглые ()", "Угловые <>"], "correct": "Фигурные {}"},
        {"id": 5, "text": "Какая функция возвращает количество элементов в коллекции или длину строки?", "variants": ["len()", "size()", "count()", "length()"], "correct": "len()"},
        {"id": 6, "text": "Какой базовый тип данных представляет целые числа в Python?", "variants": ["int", "float", "str", "bool"], "correct": "int"},
        {"id": 7, "text": "Какой тип данных используется для хранения чисел с плавающей точкой?", "variants": ["float", "int", "str", "bool"], "correct": "float"},
        {"id": 8, "text": "Какой метод позволяет добавить новый элемент в самый конец существующего списка?", "variants": ["append()", "add()", "push()", "extend()"], "correct": "append()"},
        {"id": 9, "text": "Какой цикл чаще всего применяется для итерирования по элементам списков и строк?", "variants": ["for", "while", "do-while", "repeat"], "correct": "for"},
        {"id": 10, "text": "Какая конструкция используется для безопасной обработки возникающих исключений?", "variants": ["try - except", "try - catch", "if - else", "throw - catch"], "correct": "try - except"},
        {"id": 11, "text": "Какое ключевое слово подключает внешние модули и встроенные библиотеки?", "variants": ["import", "include", "using", "require"], "correct": "import"},
        {"id": 12, "text": "Как обозначается начало однострочного комментария в скрипте на Python?", "variants": ["Символом #", "Двойным слэшем //", "Слэшем со звездочкой /*", "Тегом"], "correct": "Символом #"},
        {"id": 13, "text": "Какой метод удаляет и возвращает последний элемент списка?", "variants": ["pop()", "remove()", "clear()", "delete()"], "correct": "pop()"},
        {"id": 14, "text": "Как получить срез списка `lst` с первого по третий элементы включительно?", "variants": ["lst[0:3]", "lst[1:3]", "lst[0:4]", "lst[1:4]"], "correct": "lst[0:3]"},
        {"id": 15, "text": "Какая встроенная библиотека используется для работы с регулярными выражениями?", "variants": ["re", "math", "os", "sys"], "correct": "re"}
    ],
    "databases": [
        {"id": 1, "text": "Какое ключевое слово используется для извлечения данных из базы данных?", "variants": ["SELECT", "GET", "EXTRACT", "FETCH"], "correct": "SELECT"},
        {"id": 2, "text": "Какая команда используется для фильтрации строк в SQL-запросе?", "variants": ["WHERE", "HAVING", "FILTER", "GROUP"], "correct": "WHERE"},
        {"id": 3, "text": "Какое ключевое слово используется для сортировки результатов запроса?", "variants": ["ORDER BY", "SORT BY", "GROUP BY", "ARRANGE"], "correct": "ORDER BY"},
        {"id": 4, "text": "С помощью какой команды можно объединить две таблицы на основе общего поля?", "variants": ["JOIN", "UNION", "MERGE", "CONNECT"], "correct": "JOIN"},
        {"id": 5, "text": "Какая функция используется для подсчета количества строк в таблице?", "variants": ["COUNT()", "SUM()", "TOTAL()", "NUMBER()"], "correct": "COUNT()"},
        {"id": 6, "text": "Что расшифровывает аббревиатура SQL?", "variants": ["Structured Query Language", "Simple Queue Link", "System Query Logic", "Storage Query Laptop"], "correct": "Structured Query Language"},
        {"id": 7, "text": "Какое ключевое слово исключает дубликаты из результатов SELECT?", "variants": ["DISTINCT", "UNIQUE", "DIFFERENT", "SINGLE"], "correct": "DISTINCT"},
        {"id": 8, "text": "Какая команда используется для добавления новых записей в таблицу?", "variants": ["INSERT INTO", "ADD ROW", "UPDATE", "CREATE"], "correct": "INSERT INTO"},
        {"id": 9, "text": "Какая команда используется для изменения существующих данных в таблице?", "variants": ["UPDATE", "CHANGE", "ALTER", "MODIFY"], "correct": "UPDATE"},
        {"id": 10, "text": "Какая команда полностью удаляет таблицу из базы данных вместе со структурой?", "variants": ["DROP TABLE", "DELETE TABLE", "REMOVE TABLE", "TRUNCATE TABLE"], "correct": "DROP TABLE"},
        {"id": 11, "text": "Какое поле служит для однозначной идентификации каждой записи в таблице?", "variants": ["Первичный ключ (Primary Key)", "Внешний ключ (Foreign Key)", "Индекс", "Уникальный тег"], "correct": "Первичный ключ (Primary Key)"},
        {"id": 12, "text": "Для фильтрации агрегированных данных (после GROUP BY) используется команда...", "variants": ["HAVING", "WHERE", "WITH", "IF"], "correct": "HAVING"},
        {"id": 13, "text": "Какое ключевое слово используется для группировки данных по определенному полю?", "variants": ["GROUP BY", "ORDER BY", "SORT BY", "ALIGN BY"], "correct": "GROUP BY"},
        {"id": 14, "text": "С помощью какого оператора можно проверить значение на вхождение в диапазон?", "variants": ["BETWEEN", "IN", "LIKE", "WITHIN"], "correct": "BETWEEN"},
        {"id": 15, "text": "Какая функция возвращает среднее арифметическое значений столбца?", "variants": ["AVG()", "MEAN()", "MEDIUM()", "SUM()"], "correct": "AVG()"}
    ]
}

META_DATA = {
    'nlp': {'title': 'Основы НЛП', 'desc': 'Проверьте знания базовых понятий обработки естественного языка.', 'time': 20, 'points': ['Ключевые понятия НЛП', 'Основные задачи и подходы', 'Типы языковых ресурсов']},
    'theory': {'title': 'Теоретическая лингвистика', 'desc': 'Проверьте знания в области теоретической лингвистики.', 'time': 15, 'points': ['Базовые концепты', 'Фонетика и морфология', 'Синтаксис']},
    'translation': {'title': 'Машинный перевод', 'desc': 'Проверьте знания методов и архитектур машинного перевода.', 'time': 20, 'points': ['Нейронный и статистический перевод', 'Метрики качества', 'Архитектуры сетей']},
    'corpus': {'title': 'Корпусная лингвистика', 'desc': 'Проверьте знания по работе с текстовыми корпусами и разметкой.', 'time': 25, 'points': ['Виды корпусов', 'Методы аннотации', 'Поиск и анализ']},
    'python': {'title': 'Python для лингвистов', 'desc': 'Проверьте знания программирования на Python для анализа текстов.', 'time': 15, 'points': ['Типы данных и структуры', 'Циклы и условия', 'Функции и библиотеки']},
    'databases': {'title': 'Базы данных (SQL)', 'desc': 'Проверьте знания по работе с базами данных и написанию SQL-запросов.', 'time': 20, 'points': ['Создание запросов SELECT', 'Работа с таблицами', 'Фильтрация и объединение']}
}

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            USERS[email] = email
            session['user'] = email
            return redirect(url_for('categories'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if email in USERS:
            session['user'] = email
            return redirect(url_for('categories'))
        else:
            return "Пользователь не найден! Пожалуйста, зарегистрируйтесь."
    return render_template('login.html')

@app.route('/categories')
def categories():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('categories.html')

@app.route('/subjects')
def subjects():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('subjects.html')

@app.route('/teachers')
def teachers():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('teachers.html')

@app.route('/news')
def news():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('news.html')

@app.route('/feedback')
def feedback():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('feedback.html')

@app.route('/chatbot')
def chatbot():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html')

# МАРШРУТ ДЛЯ СТРАНИЦЫ ПРЕВЬЮ ТЕСТА
@app.route('/preview/<cat_name>')
def preview(cat_name):
    if 'user' not in session:
        return redirect(url_for('login'))
    data = META_DATA.get(cat_name)
    if not data:
        return redirect(url_for('categories'))
    total_q = len(QUESTIONS.get(cat_name, []))
    return render_template('preview.html', cat_name=cat_name, data=data, total_q=total_q)

@app.route('/start_test/<cat_name>')
def start_test(cat_name):
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    session['user_answers'] = {}
    session['last_cat'] = cat_name
    session['start_time'] = time.time() 
    
    return redirect(url_for('test', cat_name=cat_name, index=0))

@app.route('/test/<cat_name>/<int:index>', methods=['GET', 'POST'])
def test(cat_name, index):
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    questions = QUESTIONS.get(cat_name, [])
    if index >= len(questions) or index < 0:
        return redirect(url_for('result'))
    
    total_minutes = META_DATA.get(cat_name, {}).get('time', 20)
    total_seconds = total_minutes * 60

    start_time = session.get('start_time')
    if not start_time:
        session['start_time'] = time.time()
        start_time = session['start_time']

    seconds_passed = time.time() - start_time
    time_left = int(total_seconds - seconds_passed)
    
    if time_left <= 0:
        return redirect(url_for('result'))
    
    if request.method == 'POST':
        answer = request.form.get('answer')
        if 'user_answers' not in session: 
            session['user_answers'] = {}
            
        if answer:
            session['user_answers'][str(index)] = answer
            
        session.modified = True

        action = request.form.get('action')
        if action == 'next':
            return redirect(url_for('test', cat_name=cat_name, index=index + 1))
        elif action == 'finish':
            return redirect(url_for('result'))
        else:
            return redirect(url_for('test', cat_name=cat_name, index=index))
            
    current_answer = session.get('user_answers', {}).get(str(index))
    
    return render_template('test.html', 
                           category=cat_name, 
                           question=questions[index], 
                           index=index, 
                           total=len(questions),
                           current_answer=current_answer,
                           time_left=time_left)

@app.route('/result')
def result():
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    cat_name = session.get('last_cat', 'theory')
    user_answers = session.get('user_answers', {})
    questions = QUESTIONS.get(cat_name, [])
    
    score = 0
    report = []
    for i, q in enumerate(questions):
        u_ans = user_answers.get(str(i))
        is_corr = (u_ans == q['correct'])
        if is_corr: 
            score += 1
        report.append({
            'text': q['text'], 
            'user_ans': u_ans, 
            'correct_ans': q['correct'], 
            'is_correct': is_corr
        })
            
    percent = int((score / len(questions)) * 100) if questions else 0
    show_razbor = request.args.get('razbor') == 'true'
    
    return render_template('result.html', 
                           score=score, 
                           total=len(questions), 
                           percent=percent, 
                           show_razbor=show_razbor, 
                           report=report)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
