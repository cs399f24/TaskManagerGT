from flask import Flask, render_template, request

app = Flask(__name__)


# Home route
@app.route("/")
def home():
    return "<h1>Welcome to the Task Manager!</h1><p>Navigate to /hello or /greet</p>"


# Route with a dynamic name parameter
@app.route("/hello/<name>")
def hello_name(name):
    return f"<h2>Hello, {name}!</h2><p>Welcome to the personalized page.</p>"


# Route to greet based on a query parameter
@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    return f"<h2>Greetings, {name}!</h2><p>Enjoy your stay!</p>"


# Route using a template to render HTML
@app.route("/about")
def about():
    return render_template("about.html", title="About", description="This is a Flask app demo.")


if __name__ == "__main__":
    app.run(debug=True)
