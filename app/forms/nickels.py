from flask_wtf import Form
from flask.ext.login import current_user
from wtforms import (ValidationError, TextField, IntegerField)
from wtforms.validators import (DataRequired, InputRequired)
from ..models import User


class SendForm(Form):
    recipient_username = TextField (
        'Recipient',
        validators=[DataRequired()]
    )
    amount = IntegerField(
        'Amount',
        validators=[InputRequired()]
    )

    def validate_recipient_username(self, field):
        if not User.is_username_taken(username=field.data):
            raise ValidationError("That user doesn't exist!")

    def validate_amount(self, field):
        if isinstance(field.data, int):
            if field.data < 1:
                raise ValidationError("You need to send at least 1 nickel.")
            elif current_user.main_wallet.nickels == 0:
                raise ValidationError("You don't have any nickels in your wallet.")
            elif field.data > current_user.main_wallet.nickels:  # TODO: had 2 nickels, got error "you only have 2 nickels"
                raise ValidationError("You only have {0} nickels.".format(current_user.main_wallet.nickels))

    def transfer_nickels(self):
        current_user.main_wallet.subtract(self.amount.data)
        User.get_by_email_or_username(identification=self.recipient_username.data).main_wallet.add(self.amount.data)
        return self.amount.data
