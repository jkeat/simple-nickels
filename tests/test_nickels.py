from flask import url_for
from flask.ext.login import current_user
from .helpers import BaseUserTestCase


class WalletModelTests(BaseUserTestCase):
    def test_wallet_to_string(self):
        self.assertEqual(str(self.user.main_wallet), "<Wallet {0}:{1}n>".format(self.USER_USERNAME, self.WALLET_NICKELS))


class NickelsViewsTests(BaseUserTestCase):
    def test_send_nickels_page_load(self):
        self.user.confirm_email()
        self.login_user()
        response = self.client.get(url_for('nickels.send_nickels'))
        self.assert200(response, message="Send nickels page didn't load")

    def test_prevent_send_nickels_page_load_if_email_not_confirmed(self):
        self.login_user()
        response = self.client.get(url_for('nickels.send_nickels'))
        self.assert_redirects(response, url_for("users.need_confirm_email"))

    def test_prevent_send_nickels_page_load_if_anonymous(self):
        response = self.client.get(url_for('nickels.send_nickels'))
        self.assert_redirects(response, url_for("users.need_confirm_email"))

    def test_send_nickels_to_another_user(self):
        with self.client:
            self.user.confirm_email()
            self.login_user()
            self.create_second_user()
            response = self.client.post(url_for('nickels.send_nickels'),
                                        data={"recipient_username": self.USER2_USERNAME,
                                              "amount": self.WALLET_NICKELS})
            self.assert200(response)
            self.assertEqual(current_user.main_wallet.nickels, 0)
            self.assertEqual(self.user2.main_wallet.nickels, (self.WALLET_NICKELS * 2))

    def test_prevent_sending_more_nickels_than_have(self):
        with self.client:
            self.user.confirm_email()
            self.login_user()
            self.create_second_user()
            response = self.client.post(url_for('nickels.send_nickels'),
                                        data={"recipient_username": self.USER2_USERNAME,
                                              "amount": (self.WALLET_NICKELS + 1)})
            self.assert200(response)
            self.assertEqual(current_user.main_wallet.nickels, self.WALLET_NICKELS)
            self.assertEqual(self.user2.main_wallet.nickels, self.WALLET_NICKELS)