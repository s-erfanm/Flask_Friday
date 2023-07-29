from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route("/")
def index():
    return "<p>Hello, World!</p>"

# localhost:5000/user/John
@app.route('user/<name>')
def user(name):
    return f"<h1>Hello {name}</h1>"

if __name__ == "__main__":
    app.run(debug=True)