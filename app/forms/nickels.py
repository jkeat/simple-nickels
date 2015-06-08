from flask_wtf import Form
from flask.ext.login import current_user
from wtforms import (ValidationError, TextField, IntegerField)
from wtforms.validators import DataRequired

from ..models.users import User, Wallet
from ..extensions import db


class SendForm(Form):
    recipient_username = TextField (
        'Recipient',
        validators=[DataRequired()]
    )
    amount = IntegerField(
        'Amount',
        validators=[DataRequired()]  # TODO: zero, negative, decimal?
    )

    def validate_recipient_username(self, field):
        if not User.query.filter_by(username=field.data.lower()).count():
            raise ValidationError("That user doesn't exist!")

    def validate_amount(self, field):
        if current_user.main_wallet.nickels < field.data:  # TODO: had 2 nickels, got error "you only have 2 nickels"
            raise ValidationError("You only have {0} nickels :'(".format(current_user.main_wallet.nickels))

    def transfer_nickels(self):
        current_user.main_wallet.subtract(self.amount.data)
        User.query.filter_by(username=self.recipient_username.data).first().main_wallet.add(self.amount.data)
        return self.amount.data
