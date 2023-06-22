import csv
from datetime import datetime
# импортируем функцию выбора случайного значения
from random import randrange

import click
# из модуля flask импортируем класс Flask
# также импортируем функцию render_template
from flask import Flask, abort, flash, redirect, render_template, url_for
# новый импорт для создания и применения миграций
from flask_migrate import Migrate
# из модуля (расширение для flask) импортируем нужный класс
from flask_sqlalchemy import SQLAlchemy
# новые импорты для создания форм
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional

# создаем экземпляр класса Flask - объект приложения Flask
app = Flask(__name__)

# создаем подключение к БД SQLite
# для этого добавляем в настройки проекта новый ключ
# и задаем ему значение
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Задаётся конкретное значение для конфигурационного ключа
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# для всех форм включена поддержка защиты с использованием CSRF-токена
# такая защита требует секретного ключа из настроек Flask
app.config['SECRET_KEY'] = 'MY SECRET KEY FOR FORM'

# создаем экземпляр класса SQLAlchemy и в него передается
# в кач-ве параметра экземпляр приложения Flask
db = SQLAlchemy(app)
# создаем экземпляр класса Migrate
migrate = Migrate(app, db)


# описание модели
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # добавим новое поле
    added_by = db.Column(db.String(64))


# класс формы опишем сразу после модели Opinion
class OpinionForm(FlaskForm):
    # форма должна состоять из 3-ех полей - title, text, source
    # у каждого поля свой тип, который мы импортируем из модуля wtform
    # это возможно благодаря интеграции flask и  wtform

    # для каждого поля есть свой тип - например StringField
    # это значит создано поле строкового типа
    # для него указано 2 параметра - lable и  validators
    # lable - название поля, которое обычно отображается рядом с полем
    # или внутри этого поля
    # validators - список валидаторов, которые выполняет проверку
    # на то, что поля соответствуют ожидаемому результату
    # валидатор DataRequired проверяет наличие данных в поле ввода
    # валидатор Length проверяет длину строки
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )

    # для поля text также используется валидатор DataRequired
    # который проверяет наличие данных в поле ввода
    text = TextAreaField(
        'Напишите мнение',
        validators=[DataRequired(message='Обязательное поле')]
    )

    # валидатор Length проверяет длину строки
    # валидатор Optional позволяет полю source быть необязательным
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1, 256), Optional()]
    )

    submit = SubmitField('Добавить')


# добавим новую функцию обернутую в декоратор @app.cli.command
# для создания новой пользовательской консольной команды
# первым параметром передаем строку - имя команды
@app.cli.command('load_options')
def load_options_command():
    """Функция загрузки мнений в базу данных."""
    # открывается файл
    with open('opinions.csv', encoding='utf-8') as f:
        # создается итерируемый объект, который отображает каждую строку
        # в качестве словаря с ключами из шапки файла
        reader = csv.DictReader(f)
        # для подсчета строк добавляется счетчик
        counter = 0
        for row in reader:
            # распакованный словарь можно использовать
            # для создания объекта мнения
            opinion = Opinion(**row)
            # изменения нужно зафиксировать
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений: {counter}')




# после класса формы добавим новую функцию, которая будет обрабатывать
# исключение '404: страница не найдена'
# для регистрации функции-обработчика используем декоратор
# @app.errorhandler
@app.errorhandler(404)
def page_not_found(error):
    # вкачестве ответа вернется собственный шаблон и код ошибки
    return render_template('404.html'), 404


# зарегистрируем еще один обработчик - функцию, которая будет
# обрабатывать исключение "500: внутренняя ошибка сервера"
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


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
        abort(404)
        # return 'В базе данных сообщений нет.'
    # иначе выбирается случайное число в диапазоне от 0 до quantity
    offset_value = randrange(quantity)
    # и определяется случайный объект
    opinion = Opinion.query.offset(offset_value).first()
    # возврат функции
    # в функцию передаем имя шаблона(обязательный параметр)
    # и весь объект opinion
    return render_template('opinion.html', opinion=opinion)


# добавим новую функцию для добавления нового мнения о фильме
@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    # создаем экземпляр формы
    form = OpinionForm()
    # если ошибок не возникло, то
    if form.validate_on_submit():
        text = form.text.data
        # если в БД уже есть мнение о фильме с таким текстом, который ввел
        # пользователь, то:
        # (first()) вернет первую запись соответсвующего запроса
        if Opinion.query.filter_by(text=text).first() is not None:
            # вызовем функцию flash и передаем соответствующее сообщ-е
            flash('Такое мнение уже было оставлено ранее!')
            # после чего вернем пользователя на страницу с формой
            # "Добавить новое мнение"
            return render_template('add_opinion.html', form=form)

        # если же такого мнения еще не было, создаем его
        # нужно создать новый экземпляр класса Opinion
        # новый экземпляр модели, новое мнение о фильме
        # каждое поле модели = соответствующим данным, которые
        # пользователь отправил через форму
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )

        # затем добавляем этот экземпляр класса Opinion посредством сессии
        # добавляется новая запись мнения о фильме в БД
        db.session.add(opinion)
        # зафиксируем изменения в БД
        db.session.commit()
        # затем перейдем на страницу добавленного мнения
        return redirect(url_for('opinion_view', id=opinion.id))
    # иначе просто отрисовать страницу с формой
    return render_template('add_opinion.html', form=form)


# добавим новую функцию, обернутую в декоратор @app.route
# который свяжет данную функцию с указанным URL
# указываем конвертер пути для id конкретного мнения
@app.route('/opinions/<int:id>')
# сама функция. В кач-ве параметра она принимает id мнения
def opinion_view(id):
    # запрашиваем конкретное мнение по id
    opinion = Opinion.query.get_or_404(id)
    # передаем это мнение в шаблон с помощью функции
    # render_template
    return render_template('opinion.html', opinion=opinion)


# в этом блоке команда запуска приложения
if __name__ == '__main__':
    app.run()
