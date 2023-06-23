# импорт для создания и применения миграций
from flask import Flask
from flask_migrate import Migrate
# из модуля (расширение для flask) импортируем нужный класс
from flask_sqlalchemy import SQLAlchemy
from settings import Config


# создаем экземпляр класса Flask - объект приложения Flask
app = Flask(__name__)
app.config.from_object(Config)
# создаем экземпляр класса SQLAlchemy и в него передается
# в кач-ве параметра экземпляр приложения Flask
db = SQLAlchemy(app)
# создаем экземпляр класса Migrate
migrate = Migrate(app, db)

from . import api_views, cli_commands, error_handlers, views
