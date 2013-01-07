from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/SNS_Database'
db = SQLAlchemy(app)

class User1(db.Model):
    email = db.Column(db.String(30),primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
    def __init__(self,email,name,password):
        self.email = email
        self.name = name
        self.password = password

class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    email = db.Column(db.String(30),nullable=False)
    content = db.Column(db.String(300),nullable=False)
    
    def __init__(self,email,content):
        self.email = email
        self.content = content

class Friend(db.Model):
    __tablename__='friend'
    
    email = db.Column(db.String(30),db.ForeignKey('user1.email'),primary_key=True)
    friend_email = db.Column(db.String(30),nullable=False,primary_key=True)
    user1 = db.relationship('User1',backref=db.backref('friends', lazy='dynamic'))
    
    def __init__(self,email,friend_email):
        self.email = email
        self.friend_email = friend_email