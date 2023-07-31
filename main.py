from flask import Flask, render_template, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "boss ... i had a wildlife accident"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

# Create a form class
db = SQLAlchemy(app)
# create a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    # create a string
    def __repr__(self):
        return f"<Name {self.name}>"

# with app.app_context():
#     db.create_all()
# Create a Form Class
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a Form Class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")


# Create a route decorator
@app.route("/")
def index():
    return render_template("index.html")

# localhost:5000/user/John
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user=name)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user = Users(name=form.name.data, email=form.email.data)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.email.data = ''
		flash("User Added Successfully!")
	our_users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html",
		form=form,
		name=name,
		our_users=our_users)



# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html",
				form=form,
				name_to_update = name_to_update)
		except:
			flash("Error!  Looks like there was a problem...try again!")
			return render_template("update.html",
				form=form,
				name_to_update = name_to_update)
	else:
		return render_template("update.html",
				form=form,
				name_to_update = name_to_update)




# CREATE custome error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal sever error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Create Name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template("name.html",
                           name=name,
                           form=form)


if __name__ == "__main__":
    app.run(debug=True)