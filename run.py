from Election import app,db
from Election.models import Option, Global

if __name__ == '__main__':
	db.create_all()

	choice = Option(one =0 ,two = 0, three = 0, four = 0 )
	db.session.add(choice)


	world = Global(username = 'Chloe' , key = 1111 , userid = 1)
	db.session.add(world)

	db.session.commit()
	app.run()
