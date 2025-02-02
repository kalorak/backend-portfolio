from flask import Flask, render_template, request, g, send_from_directory, url_for
import sqlite3
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

DATABASE = "contact.db"

# Function to get a database connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Ensure results can be accessed like dictionaries
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
        {"name": "To-Do App", "description": "A simple task management app built with Python and Flask. (in development)"},
        {"name": "Blog API", "description": "A RESTful API for a blogging platform. (in development)"},
    ]
    return render_template("projects.html", projects=project_list)

# Contact route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        if name and message:
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

# Static files route (for CSS, JS, images)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Close the database connection when the app shuts down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))