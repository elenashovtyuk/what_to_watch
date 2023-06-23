from flask import render_template

from . import app, db


# добавим новую функцию, которая будет обрабатывать
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
    db.session.rollback()
    return render_template('500.html'), 500
