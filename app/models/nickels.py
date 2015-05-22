from ..extensions import db
from users import User


class Wallet(db.Model):
    __tablename__ = 'wallet'

    id = db.Column(db.Integer, primary_key=True)
    nickels = db.Column(db.Integer)  # nickels are lowest denomination
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # may have multiple wallets later on, so not one-to-one
    user = db.relationship(User, backref=db.backref('wallets',
                                                    uselist=True,
                                                    cascade='delete,all'))

    def __repr__(self):
        return '<Wallet {0}:{1}n>'.format(self.user.username, self.nickels)
