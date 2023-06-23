# новые импорты для создания форм
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


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
