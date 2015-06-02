from flask_wtf import Form
from flask import current_user
from wtforms import ValidationError, TextField, IntegerField
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
		validators=[DataRequired()]
	)

	def validate_recipient_username(self, field):
		if User.query.filter_by(
                username=field.data.lower()).count():
            raise ValidationError("That user doesn't exist!")

    def validate_amount(self, field):
    	if current_user.main_wallet.nickels < field.data:
    		raise ValidationError("You only have {0} nickels!".format(field.data))

    def transfer_nickels(self):
    	current_user.main_wallet.subtract(self.amount.data)
    	User.query.filter_by(username=recipient_username).main_wallet.add(self.amount.data)
