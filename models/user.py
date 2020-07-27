import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(100))
    
    def __init__(self, username, password):
        # self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        return user

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # sql = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(sql, (username,))
        # row = result.fetchone()
        
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None

        # connection.close()
        # return user

    @classmethod
    def find_by_id(cls, _id):
        user = cls.query.filter_by(id=_id).first()
        return user
        
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # sql = "SELECT * FROM users WHERE id = ?"
        # result = cursor.execute(sql, (_id,))
        # row = result.fetchone()

        # if row:
        #     user = cls(*row)
        # else:
        #     user = None

        # connection.close()
        # return user

    def json(self):
        return {
            'id': self.id,
            'username': self.username
            }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
