from ..extensions import db


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
        return '<Wallet {0}:{1}n>'.format(self.user.username, self.nickels)
