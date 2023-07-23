from flask import Flask, render_template, redirect, session, request, flash
from wtforms import Form, StringField, PasswordField, validators
from database import create_user, check_user
import secrets
# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Set the secret key for the Flask application
secret_key = secret_key

app = Flask(__name__)

class UserForm(Form):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    # Handle login form submission here (perform validation and authentication)
    # For simplicity, we'll assume any username and password combination is valid
    session['username'] = request.form['username']
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect('/')


@app.route('/')
def MindNex():
    if 'username' in session:
        return redirect('/dashboard')
    else:
        return redirect("/create_user")


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        # Handle the form submission for creating a user
        # Extract the form data and insert it into the database
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Call the function to create the user in the database (using database.py)
        if create_user(username, email, password):
            # If user creation is successful, redirect to the dashboard
            session['username'] = username
            return redirect('/dashboard')
        else:
            # If user creation fails, show an error message
            flash("Error creating user.", "error")

    return render_template("home.html")

if __name__ == "__main__":
    app.run(port=5000)
