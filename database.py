from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import ProgrammingError
from config.config import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE

# Construct the connection string
connection_string = f'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

# Create the engine
engine = create_engine(connection_string)

# Create the inspector
inspector = inspect(engine)

# Function to create a new user in the database
def create_user(username, email, password):
    try:
        # Insert the user data into the users table
        with engine.connect() as conn:
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            conn.execute(query, (username, email, password))

        return True  # User created successfully
    except ProgrammingError as error:
        print(f"Error creating user: {error}")
        return False  # Error creating user

# Function to check if a user exists and validate the password
def check_user(username, password):
    try:
        # Check if the user exists in the database
        with engine.connect() as conn:
            query = "SELECT * FROM users WHERE username = %s"
            result = conn.execute(query, (username,))
            user = result.fetchone()

        if user is None:
            return False  # User does not exist

        # Validate the password
        _, _, hashed_password = user
        if password == hashed_password:
            return True  # Login successful
        else:
            return False  # Incorrect password

    except ProgrammingError as error:
        print(f"Error checking user: {error}")
        return False  # Error checking user

# Add more functions for other database operations if needed
