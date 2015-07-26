from flask import (render_template, Blueprint)


pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
    return render_template('pages/home.html')


@pages.route('/about')
def about():
    return render_template('pages/about.html')
