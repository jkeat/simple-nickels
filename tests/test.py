import unittest
from flask import url_for
from flask.ext.testing import TestCase
from flask.ext.login import login_user, current_user
from app import create_app, User, Wallet
from app.extensions import db, mail


class BaseTestCase(TestCase):
    USER_USERNAME = "homer"
    USER_EMAIL = "hsimpson@donutmail.net"
    USER_PASSWORD = "marge4life"

    USER2_USERNAME = "lisa"
    USER2_EMAIL = "lisa2000@rocketmail.com"
    USER2_PASSWORD = "nelson_is_ha_hawt"

    WALLET_NICKELS = 3

    def create_app(self):
        app = create_app('config.testing')
        return app

    def setUp(self):
        db.create_all()
        self.user = self.create_user(self.USER_USERNAME,
                                     self.USER_EMAIL,
                                     self.USER_PASSWORD)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user(self, username, email, password):
        user = User(username=username,
                    email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        user_id = User.query.filter_by(username=username).first().id
        wallet = Wallet(nickels=self.WALLET_NICKELS,
                        user_id=user_id)
        db.session.add(wallet)
        db.session.commit()
        return user

    def create_second_user(self):
        self.user2 = self.create_user(self.USER2_USERNAME,
                                      self.USER2_EMAIL,
                                      self.USER2_PASSWORD)

    def login_user(self):
        self.client.post(url_for('users.login'),
                         data={"username": self.USER_USERNAME,
                               "password": self.USER_PASSWORD},
                         follow_redirects=True)

    def logout_user(self):
        self.client.post(url_for('users.logout'),
                         follow_redirects=True)


class PageViewsTests(BaseTestCase):
    def test_about_page_load(self):
        response = self.client.get(url_for('pages.about'))
        self.assert200(response, message="About page didn't load")

    def test_home_page_load(self):
        response = self.client.get(url_for('pages.home'))
        self.assert200(response, message="Home page didn't load")


class UserViewsTests(BaseTestCase):
    def test_register_page_load(self):
        response = self.client.get(url_for('users.register'))
        self.assert200(response, message="Signup page didn't load")

    def test_login_page_load(self):
        response = self.client.get(url_for('users.login'))
        self.assert200(response, message="Log in page didn't load")

    def test_can_user_register(self):
        with self.client:
            user_data = {"username": self.USER2_USERNAME,
                         "email": self.USER2_EMAIL,
                         "password": self.USER2_PASSWORD,
                         "confirm": self.USER2_PASSWORD}
            response = self.client.post(url_for("users.register"),
                                        data=user_data)
            self.assert_redirects(response, url_for("pages.home"))

    def test_prevent_user_registering_with_taken_username(self):
        with self.client:
            user_data = {"username": self.USER_USERNAME,
                         "email": self.USER2_EMAIL,
                         "password": self.USER2_PASSWORD,
                         "confirm": self.USER2_PASSWORD}
            response = self.client.post(url_for("users.register"),
                                        data=user_data)
            self.assert200(response)
            self.assertIsNone(User.query.filter_by(email=self.USER2_EMAIL).first())

    def test_can_user_login_with_username(self):
        with self.client:
            response = self.client.post(url_for('users.login'),
                                        data={"username": self.USER_USERNAME,
                                              "password": self.USER_PASSWORD})
            self.assert_redirects(response, url_for("pages.home"))
            self.assertEqual(current_user.username, self.USER_USERNAME)

    def test_can_user_login_with_email(self):
        with self.client:
            response = self.client.post(url_for('users.login'),
                                        data={"username": self.USER_EMAIL,
                                              "password": self.USER_PASSWORD})
            self.assert_redirects(response, url_for("pages.home"))
            self.assertEqual(current_user.username, self.USER_USERNAME)


class NickelsViewsTests(BaseTestCase):
    def test_send_nickels_page_load(self):
        with self.client:
            self.user.confirm_email()
            self.login_user()
            response = self.client.get(url_for('nickels.send_nickels'))
            self.assert200(response, message="Send nickels page didn't load")

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


if __name__ == '__main__':
    unittest.main()
