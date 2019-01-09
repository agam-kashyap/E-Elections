from Election import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique=True, nullable = False)
	password = db.Column(db.String(60), nullable = False)
	votedid = db.Column(db.Integer)

class Option(db.Model, UserMixin):
	__bind_key__ = "two"
	id = db.Column(db.Integer , primary_key = True)
	one = db.Column(db.Integer)
	two = db.Column(db.Integer)
	three = db.Column(db.Integer)
	four = db.Column(db.Integer)

class Candidate(db.Model, UserMixin):
	__bind_key__ = "three"
	id = db.Column(db.Integer , primary_key = True)
	username = db.Column(db.String(20) , unique = False , nullable = False )
	password = db.Column(db.String(8), nullable = False)
	key = db.Column(db.Integer, unique = True , nullable = False)

class Cand_info(db.Model, UserMixin):
	__bind_key__ = "four"
	id = db.Column(db.Integer , primary_key = True)
	info = db.Column(db.Text, nullable = False)
	facebook = db.Column(db.String(90), nullable = True)
	github = db.Column(db.String(90), nullable = True)

class Global(db.Model):
	__bind_key__ = "five"
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(40) , nullable = False)
	key = db.Column(db.Integer , nullable = False)
	userid = db.Column(db.Integer , nullable = False)