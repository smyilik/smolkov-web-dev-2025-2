import random
from functools import lru_cache
from flask import Flask, render_template
from faker import Faker

fake = Faker()

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

app = Flask(__name__)
application = app

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

if __name__ == "__main__":
    app.run(debug=True)