import random
from functools import lru_cache
from flask import request
from flask import Flask, make_response, render_template, session, flash, g, redirect, url_for
from faker import Faker
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

DATABASE = 'web_db.db'
SECRET_KEY = 'f905fa91afe84294ea89da342c0b46b20fd133c5'
DEBUG = True
fake = Faker()

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'web_db.db')))
app.config['SECRET_KEY'] = SECRET_KEY
application = app

login_manager = LoginManager(app)

def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    # data will be represented as dictionary instead of tuple
    connection.row_factory = sqlite3.Row
    return connection

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as file:
        # Cursor class provides methods for moving the cursor
        # through the query result, and methods to get the data
        # from the columns of each row in the result
        db.cursor().executescript(file.read())
    # Save changes to database and close it
    db.commit()
    db.close()

def get_db():
    # check if g has attribute 'link_db'
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
g_user = None

@app.before_request
def before_request_function():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.teardown_appcontext
def close_db(error):
    # check if g has attribute 'link_db'
    if hasattr(g, 'link_db'):
        g.link_db.close()

@login_manager.user_loader
def load_user(user_id):
    # print('load_user')
    return UserLogin().fromDB(user_id, dbase)

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = { 
            'author': fake.name(),
            'text': fake.text(),
            'date': fake.date_time_between(start_date='-2y', end_date='now'),
            'time': fake.time()
        }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': fake.random.choice(('10 способов повысить продуктивность уже сегодня',
                                     'Как начать своё утро правильно: советы экспертов',
                                     'Топ-5 книг, которые изменят ваше мышление',
                                     'Почему важно выходить из зоны комфорта',
                                     'Лайфхаки для тех, кто хочет больше успевать',
                                     'Как сохранить мотивацию в трудные времена',
                                     'Секреты успешных людей: чему у них можно научиться',
                                     'Простые привычки, которые улучшат вашу жизнь',
                                     'Что мешает вам достичь целей и как это исправить',
                                     'Истории людей, которые доказали, что всё возможно')),
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

def check_phone_number(phone_number):
    # 10-11 numbers
    # must start with +7 or 8 if has 11 numbers
    # else does not have to
    extra_symbols = [' ', '(', ')', '-', '.', '+']
    numbers = ""
    phone_number.replace(' ', '')
    phone_number.replace('(', '')
    phone_number.replace(')', '')
    phone_number.replace('-', '')
    phone_number.replace('.', '')
    is_plus_first = False
    if phone_number[0] == '+':
        is_plus_first = True
    phone_number.replace('+', '')
    for symbol in phone_number:
        if not(symbol.isdigit()) and symbol not in extra_symbols:
            return "Недопустимый формат. Указаны недопустимые символы."
        elif symbol.isdigit():
            numbers += symbol
    if len(numbers) > 11 or len(numbers) < 10:
        return "Недопустимый формат. Неверное количество цифр в номере телефона."
    elif len(numbers) == 11 and (numbers[0] != '8' and (numbers[0] != '7' or not(is_plus_first))):
        return "Недопустимый формат. Неверное начало номера."
    return None

def convert_phone_number(phone_number):
    # 8-***-***-**-**
    # ***-***-**-**
    numbers = ""
    for symbol in phone_number:
        if symbol.isdigit():
            numbers += symbol
    result = ""
    if len(numbers) == 11:
        result = "8-" + numbers[1:4] + "-" + numbers[4:7] + "-" + numbers[7:9] + "-" + numbers[9:11]
    else:
        result = numbers[0:3] + "-" + numbers[3:6] + "-" + numbers[6:8] + "-" + numbers[8:10]
    return result

@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list())

@app.route('/posts/<int:index>')
def post(index):
    p = posts_list()[index]
    return render_template('post.html', title=p['title'], post=p)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.route('/url_arguments')
def url_arguments():
    return render_template('url_arguments.html', title='Параметры Url')

@app.route('/request_headers')
def request_headers():
    return render_template('request_headers.html', title='Заголовки запроса')

@app.route('/cookie')
def cookie():
    if request.cookies.get("Test-cookie"):
        response = make_response(render_template('cookie.html', title='Cookie'))
        response.set_cookie("Test-cookie", "", expires=0)
    else:
        response = make_response(render_template('cookie.html', title='Cookie'))
        response.set_cookie("Test-cookie", "123")
    return response

@app.route('/form_parameters', methods=['GET','POST'])
def form_parameters():
    return render_template('form_parameters.html', title='Параметры формы')

@app.route('/phone', methods=['GET','POST'])
def phone():
    error = None
    converted_phone = None
    if request.method == 'POST':
        phone = request.form.get('phone')
        error=check_phone_number(phone)
        converted_phone=convert_phone_number(phone)
    return render_template('phone.html', title='Оставить номер', error=error,converted_phone=converted_phone)

@app.route('/session_counter')
def session_counter():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template('session_counter.html', title='Счётчик посещений')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        user = dbase.getUserByUsername(request.form['username'])
        if user and check_password_hash(user['password'], request.form['password']):
            global g_user
            g_user = UserLogin().create(user)
            login_user(g_user)
            return render_template('index.html')
        # makes it possible to record a message at the end of a request and access it next request and only next request
        # used to give feedback to a user
        error = "Wrong password or login"
    return render_template('login.html', title='Log in', error=error)

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    error = None
    if request.method == "POST":
        # if len(request.form['username']) > 4 and len(request.form['email']) > 4 \
        #     and len(request.form['password'] > 4):
        hash = generate_password_hash(request.form['password'])
        res = dbase.addUser(request.form['username'], request.form['email'], hash)
        if res:
            user = dbase.getUserByUsername(request.form['username'])
            global g_user
            g_user = UserLogin().create(user)
            login_user(g_user)
            return render_template('index.html')
        else:
            error = "User with this email already exists"
    return render_template("reg.html", title="Регистрация", error=error)



# if __name__ == "__main__":
#     app.run(debug=DEBUG)
