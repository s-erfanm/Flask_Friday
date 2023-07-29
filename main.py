from flask import Flask, render_template, url_for, flash
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
# CREATE A Form Class
class SubmitForm(FlaskForm):
    name = StringField("what is your name ? ", validators=[DataRequired()])
    submit = SubmitField("submit")


# Create a route decorator
@app.route("/")
# def index():
#     return "<p>Hello, World!</p>"
def index():
    creator_name = "s.erfan.m"
    foods = ["Pizza", "Felafel", "Pasta", "Kebab"]

    return render_template("index.html", creator_name=creator_name, all_foods=foods)

# localhost:5000/user/John
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user=name)

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
@app.route('/name/', methods=['POST','GET'])
def name():
    name = None
    form = SubmitForm()
    # Validate From
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted successfully")
    return render_template("name.html",name=name, form=form)



if __name__ == "__main__":
    app.run(debug=True)