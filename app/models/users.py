import os
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import or_
from ..extensions import db


class User(db.Model):
    # TODO: accessor for 'main wallet'

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(255), unique=True)
    passhash = db.Column(db.String(255))
    confirmed_email = db.Column(db.Boolean(), default=False)

    wallets = db.relationship("Wallet", backref="user")


    @property
    def main_wallet(self):
        return self.wallets[0]
    
    def __init__(self, username, email, password):
        self.username = username.lower()
        self.email = email.lower()
        self.set_password(password)

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def set_password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

    def confirm_email(self):
        self.confirmed_email = True
        db.session.add(self)
        db.session.commit()

    # ========= Flask-Login required methods vvv
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    # ========= end Flask-Login required methods ^^^

    @classmethod
    def get_by_email_or_username(cls, identification):
        return cls.query.filter(or_(cls.username == identification,
                                    cls.email == identification)).first()


class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    # nickels are lowest denomination; no fractions of nickels
    nickels = db.Column(db.Integer)
    # one to many; however currently users have only one wallet
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def add(self, amount):
        self.nickels += amount
        db.session.commit()

    def subtract(self, amount):
        self.nickels -= amount
        db.session.commit()


    def __init__(self, nickels, user_id):
        self.nickels = nickels
        self.user_id = user_id

    def __repr__(self):
        return '<Wallet contains: {0}n>'.format(self.nickels)
