import csv

import click

from . import app, db
from .models import Opinion


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
