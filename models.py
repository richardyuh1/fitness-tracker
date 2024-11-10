# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Page(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    events = db.Column(db.String(500), unique=False, nullable=True)

    def __repr__(self):
        return f'<Page {self.id}>'
