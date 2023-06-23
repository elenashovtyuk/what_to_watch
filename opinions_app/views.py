# импортируем функцию выбора случайного значения
from random import randrange
from flask import abort, flash, redirect, render_template, url_for
from . import app, db
from .forms import OpinionForm
from .models import Opinion


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
