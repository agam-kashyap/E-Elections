from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder = 'Template')
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_BINDS'] = { 'two' : 'sqlite:///votes.db', 'three' : 'sqlite:///candidates.db', 'four' : 'sqlite:///cand-info.db' , 'five' : 'sqlite:///global.db'}
app.config['SERVER_NAME'] = 'localhost:8080'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from Election import routes