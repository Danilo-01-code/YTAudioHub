from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, DateField
from flask_login import UserMixin
from datetime import date

db = SqliteDatabase("database.db")

class Users(Model, UserMixin):
    username = CharField(unique=True)
    password = CharField()  

    class Meta:
        database = db

class Audios(Model,UserMixin):
    title = CharField(unique = True)
    path = CharField(unique = True)
    category = CharField()
    author = CharField()
    date = DateField(default=date.today)
    user = ForeignKeyField(Users, backref='audios')
    
    class Meta:
        database = db
