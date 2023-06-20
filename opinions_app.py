from datetime import datetime

# импортируем функцию выбора случайного значения
from random import randrange

# из модуля flask импортируем класс Flask
# также импортируем функцию render_template
from flask import Flask, render_template

# из модуля (расширение для flask) импортируем нужный класс
from flask_sqlalchemy import SQLAlchemy

# создаем экземпляр класса Flask - объект приложения Flask
app = Flask(__name__)

# создаем подключение к БД SQLite
# для этого добавляем в настройки проекта новый ключ
# и задаем ему значение
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# Задаётся конкретное значение для конфигурационного ключа
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# создаем экземпляр класса SQLAlchemy и в него передается
# в кач-ве параметра экземпляр приложения Flask
db = SQLAlchemy(app)


# описание модели
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


# функция с основной логикой обернутая в декоратор app.route,
# который связывает функцию с указанным URL('/')
# эта функция отвечает за отображение главной страницы
@app.route('/')
def index_view():
    # определяем общее кол-во мнений в базе данных
    quantity = Opinion.query.count()
    # если мнений нет
    if not quantity:
        # то возвращается сообщение
        return 'В базе данных сообщений нет.'
    # иначе выбирается случайное число в диапазоне от 0 до quantity
    offset_value = randrange(quantity)
    # и определяется случайный объект
    opinion = Opinion.query.offset(offset_value).first()
    # возврат функции
    # в функцию передаем имя шаблона(обязательный параметр)
    # и весь объект opinion
    return render_template('opinion.html', opinion=opinion)


# добавим новую функцию для добавления нового мнения о фильме
@app.route('/add')
def add_opinion_view():
    return render_template('add_opinion.html')
    # return 'Совсем скоро тут будет случайное мнение о фильме!'


# в этом блоке команда запуска приложения
if __name__ == '__main__':
    app.run()
