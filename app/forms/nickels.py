from flask_wtf import Form
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
    	user = User.query.filter_by(username=self.recipient_username.data.lower())
    	if user.wallets[0].nickels < field.data:
    		raise ValidationError("You only have {0} nickels!".format(field.data))

    def transfer_nickels(self):
    	# TODO: subtract nickels from current_user's wallet and add to recipient's.
    	pass