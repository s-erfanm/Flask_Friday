from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)