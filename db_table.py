from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import secrets

secret_key = secrets.token_hex(16)
print(secret_key)

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://avnadmin:AVNS_JTEBOpKYpRGXaDu4lwv@mysql-285s-atm-machine-project.b.aivencloud.com:13765/defaultdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(50), nullable=True)

    accounts = db.relationship('Bank', backref='user', lazy=True)


class Bank(db.Model):
    __tablename__ = 'Bank'
    acc_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    accounts = db.relationship('ATM', backref='bank', lazy=True)


class ATM(db.Model):
    __tablename__ = 'ATM'
    row_id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(10), nullable=False)
    balance = db.Column(db.Integer, nullable=True)

    pin_id = db.Column(db.Integer, db.ForeignKey('Bank.acc_id'), nullable=False)


with app.app_context():
    db.create_all()