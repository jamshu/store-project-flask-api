from db import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
