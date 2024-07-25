from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_sqlalchemy.model import Model
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

Download_PATH = 'wkhtmltopdf/bin/wkhtmltopdf' #cambio de wkhtmltopdf/bin/wkhtmltopdf
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
Download_FOLDER = os.path.join(APP_ROOT, Download_PATH)


from webapp import routes