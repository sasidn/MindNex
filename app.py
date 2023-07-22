from flask import Flask, render_template, redirect, session, request
from wtforms import Form, StringField, PasswordField, validators

app = Flask(__name__)

class UserForm(Form):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])


@app.route('/')
def index():
    # Assuming you have some data you want to display on the template
    title = "Welcome to MindNex"
    description = "Explore the nexus of mind and potential"

    # You can also include more data like the URL of the logo and banner images
    logo_url = "/static/logo/MindNexLog.png"
    banner_url = "/static/wallpaper/home.jpg"

    # Include the data in the context dictionary
    context = {
        "title": title,
        "description": description,
        "logo_url": logo_url,
        "banner_url": banner_url,
        # Add more data as needed
    }
    return render_template('home.html', **context)


@app.route('/')
def MindNex():
    if "username" in session:
        return redirect("/dashboard")
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

        # Insert the user data into the MySQL table
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)
        try:
            cursor.execute(query, values)
            db.commit()
            print("User inserted successfully!")
            flash("User created successfully!", "success")

            print("Username:", username)
        except mysql.connector.Error as error:
            print(f"Error creating user: {error}")
            flash(f"Error creating user: {error}", "error")

        return redirect("/")

    return render_template("home.html")


@app.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        email = request.form["email"]

        # Check if the email exists in the database
        query = "SELECT username, password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            username = result[0]
            password = result[1]

            # Send the password reminder email
            send_password_email(email, username, password)
            flash("Password reminder sent to your email!", "success")
        else:
            flash("Email not found!", "error")

        return redirect("/")

    return render_template("forget_password.html")


def send_password_email(email, username, password):
    msg = Message("Password Reminder", sender="your_email@example.com", recipients=[email])
    msg.body = f"Hello {username},\n\nYour password is: {password}\n\nBest regards,\nMindCare Team"
    mail.send(msg)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # Query the database to fetch the user's password based on the username
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]

        # Verify the password
        if password == stored_password:
            # Successful login
            session['username'] = username
            return redirect("/dashboard.html")

    # Invalid login
    flash("Invalid username or password", "error")
    return redirect("/")


@app.route("/dashboard.html")
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard.html", username=username)
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(port=5000)
