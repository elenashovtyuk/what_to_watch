import os


class Config(object):
    # создаем подключение к БД SQLite
    # для этого добавляем в настройки проекта новый ключ
    # и задаем ему значение
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    # Задаётся конкретное значение для конфигурационного ключа
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # для всех форм включена поддержка защиты с использованием CSRF-токена
    # такая защита требует секретного ключа из настроек Flask
    SECRET_KEY = os.getenv('SECRET_KEY')
