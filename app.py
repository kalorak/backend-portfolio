from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

DATABASE = "contact.db"

# Function to get a database connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# About route
@app.route("/about")
def about():
    return render_template("about.html")

# Projects route
@app.route("/projects")
def projects():
    project_list = [
        {"name": "Portfolio Website", "description": "A Flask-powered website to showcase my backend skills."},
        {"name": "To-Do App", "description": "A simple task management app built with Python and Flask."},
        {"name": "Blog API", "description": "A RESTful API for a blogging platform."},
    ]
    return render_template("projects.html", projects=project_list)

# Contact route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]

        # Insert form data into the database
        db = get_db()
        db.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
        db.commit()

        return f"Thank you, {name}! Your message has been saved."

    return render_template("contact.html")

# Messages route to display all saved messages
@app.route("/messages")
def messages():
    db = get_db()
    cur = db.execute("SELECT name, message, timestamp FROM messages ORDER BY timestamp DESC")
    messages = cur.fetchall()
    return render_template("messages.html", messages=messages)

# Close the database connection when the app shuts down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)