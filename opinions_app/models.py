from datetime import datetime

from . import db


# описание модели мнения о фильме
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # добавим новое поле для того, чтобы пользователь мог указать имя
    added_by = db.Column(db.String(64))
