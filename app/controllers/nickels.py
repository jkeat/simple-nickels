from flask import (render_template, Blueprint, request,
                   redirect, url_for, flash)
from flask.ext.login import current_user
from ..forms.nickels import SendForm
from ..models.users import User, Wallet
from ..decorators import confirmed_email_required


nickels = Blueprint('nickels', __name__)


@nickels.route('/send', methods=['GET', 'POST'])
@confirmed_email_required
def send_nickels():
	form = SendForm()

	if request.method == 'POST':
		if not form.validate():
			return render_template('nickels/forms/send.html', form=form)
		else:
			amount = form.transfer_nickels()
			s_if_plural = "s"
			if amount == 1:
				s_if_plural = ""
			flash("Successfully transfered {0} nickel{1}!".format(amount, s_if_plural))
			return render_template('nickels/forms/send.html', form=form)

	elif request.method == 'GET':
		return render_template('nickels/forms/send.html', form=form)
