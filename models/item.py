# import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'price': self.price, 
            'store_id': self.store_id
            }

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # sql = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(sql, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     # return {'Item': {'name': row[0], 'price': row[1]}}
        #     return cls(*row)

        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # def insert(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     sql = "INSERT INTO items VALUES(?, ?)"
    #     cursor.execute(sql, (self.name, self.price))
    #     connection.commit()
    #     connection.close()
    
    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     sql = "UPDATE items SET price=? WHERE name=?"
    #     cursor.execute(sql, (self.price, self.name))
    #     connection.commit()
    #     connection.close()


    