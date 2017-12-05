from flask import render_template, current_app
from . import main
from flask_login import current_user

@main.route('/')
def index():
	return render_template('index.html')
