from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route("/")
def index():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(debug=True)