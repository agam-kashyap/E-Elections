from flask import render_template, url_for, redirect ,flash, request
from Election import app,db,bcrypt
from Election.models import User,Option, Candidate, Cand_info, Global
from flask_login import login_user, current_user, logout_user
from Election.forms import RegistrationForm, LoginForm, CandidateLoginForm, CandidateInfo

from Election.graph import build_graph


@app.route("/",methods = ['GET','POST'])
@app.route("/home",methods = ['GET','POST'])
def home():
	return render_template('home.html')

@app.route("/about", methods = ['GET','POST'])
def about():
	return render_template("about.html", title = 'About')

@app.route("/register", methods = ['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,password = hash_password)
		db.session.add(user)
		db.session.commit()
		flash("{} user registered".format(user.username),'success')
		return redirect(url_for('register'))
	return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ['GET','POST'])
def login():
	return render_template("login.html", title="Login")

@app.route("/candidatelogin", methods = ['GET','POST'])
def candidatelogin():
	form = CandidateLoginForm()
	if form.validate_on_submit():
		user = Candidate.query.filter_by(username = form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data) and user.key == form.key.data:
			login_user(user)
			world = Global.query.get(1)
			world.username = user.username
			world.key = user.key
			world.userid = user.id
			db.session.commit()
			flash(f"Welcome {form.username.data}",'success')
			return redirect(url_for('viewaboutcandidate'))
		else:
			flash('Unsuccessful login! Check your username, password and key.','danger')
	return render_template("candidatelogin.html", title="Candidate Login" , form = form)

@app.route("/candidateinfo", methods = ['GET', 'POST'])
def candidateinfo():
	form = CandidateInfo()
	userid = current_user.id
	if form.validate_on_submit():
		about = Cand_info.query.get(userid)
		about.info = form.info.data
		about.facebook = form.facebook.data
		about.facebook = form.facebook.data
		db.session.commit()
		return redirect(url_for('thankyou'))
	
	return render_template("candidateinfo.html", title = "Candidate Info", form = form)

@app.route("/candidateupdateinfo", methods = ['GET','POST'])
def candidateupdateinfo():
	#put a check for user
	id = current_user.id
	form = CandidateInfo()
	userid = current_user.id
	if form.validate_on_submit():
		newabout = Cand_info.query.get(userid)
		newabout.info = form.info.data
		newabout.facebook = form.facebook.data
		newabout.github = form.github.data
		db.session.commit()
		return redirect(url_for('candidateupdateinfo'))
	about = Cand_info.query.get(userid)
	form.info.data = about.info
	form.facebook.data = about.facebook 
	form.github.data = 	about.github  
	return render_template("candidateupdateinfo.html", title = "Update", form= form)

@app.route("/thankyou", methods = ['GET','POST'])
def thankyou():
	return render_template("thankyou.html")

@app.route("/viewaboutcandidate", methods = ['GET'])
def viewaboutcandidate():
	about = Cand_info.query.get(current_user.id)
	user = Candidate.query.get(current_user.id)
	world = Global.query.get(1)
	if world.key == 0:
		flash("Sorry, you do not have access to that page.",'danger')
		return redirect(url_for('home'))
	else:
		return render_template("viewaboutcandidate.html", title = "index", infos = about , user = user )

@app.route("/voterlogin", methods= ['GET','POST'])
def voterlogin():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			world = Global.query.get(1)
			world.username = user.username
			world.key = 0
			world.userid = user.id
			db.session.commit()
			flash(f'Welcome {form.username.data}','success')
			return redirect(url_for('categories'))
		else:
			flash('Unsuccessful login. Check your username and password','danger')
	return render_template("voterlogin.html", title="Voter Login" , form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/categories", methods = ['GET','POST'])
def categories():
	if current_user.is_authenticated:
		return render_template("categories.html" , title = "Categories")

@app.route("/presidentchoose", methods = ['GET','POST'])
def presidentchoose():
	if current_user.is_authenticated:
		return render_template("presidentchoose.html", title = "President")

@app.route("/aboutpresident", methods = ['GET','POST'])
def aboutpresident():
	about = Cand_info.query.all()
	user = Candidate.query.all()
	a = range(len(about))
	return render_template("aboutpresident.html", title= "Candidates", infos = about , users = user, num = a)

@app.route("/options", methods = ['GET','POST'])
def options():
	if current_user.is_authenticated:
		about = Cand_info.query.all()
		user = Candidate.query.all()
		candidate = Candidate.query.filter_by(username = current_user.username).first()
		world = Global.query.get(1)
		if current_user.votedid == 1011 and world.key == 0:
			return render_template("optionvoted.html")
		elif world.key != 0 :
			return redirect(url_for("candidatenovote"))
		else:
			option = request.form.get('options')
			
			if option == "one":
				choice = Option.query.get(1)
				choice.one += 1
				user = User.query.filter_by(username = current_user.username).first()
				user.votedid = 1011
				db.session.commit()
				if user.votedid == 1011:
					return redirect(url_for('optionvoted'))
				else:
					return redirect(url_for('options'))
			
			if option == "two":
				choice = Option.query.get(1)
				choice.two += 1
				user = User.query.filter_by(username = current_user.username).first()
				user.votedid = 1011
				db.session.commit()
				if user.votedid == 1011:
					return redirect(url_for('optionvoted'))
				else:
					return redirect(url_for('options'))

			if option == "three":
				choice = Option.query.get(1)
				choice.three += 1
				user = User.query.filter_by(username = current_user.username).first()
				user.votedid = 1011
				db.session.commit()
				if user.votedid == 1011:
					return redirect(url_for('optionvoted'))
				else:
					return redirect(url_for('options'))
			
			if option == "four":
				choice = Option.query.get(1)
				choice.four += 1
				user = User.query.filter_by(username = current_user.username).first()
				user.votedid = 1011
				db.session.commit()
				if user.votedid == 1011:
					return redirect(url_for('optionvoted'))
				else:
					return redirect(url_for('options'))

		a = range(len(about))
		return render_template("options.html", title= "Options", users = user, num = a)

@app.route("/optionvoted")
def optionvoted():
	world = Global.query.get(1)
	return render_template("optionvoted.html" , key = world.key)

@app.route("/candidatenovote")
def candidatenovote():
	return render_template("candidatenovote.html")

@app.route("/results")
def results():
	vote = Option.query.get(1)
	y = [vote.one,vote.two,vote.three,vote.four]
	x = ['Chloe M.','Olivia A.','James H.','Luke C.']
	graph_url = build_graph(x,y)
	return render_template("results.html", graph1 = graph_url)