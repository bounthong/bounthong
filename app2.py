from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# Database configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),           # Database host
    'user': os.getenv('DB_USER'),           # Database username
    'password': os.getenv('DB_PASSWORD'),   # Database password
    'database': os.getenv('DB_NAME')        # Database name
}


# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Root endpoint
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"})

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content, to avoid 404 errors for favicon

@app.route('/favicon.png')
def favicon_png():
    return '', 204  # No Content


# GET endpoint to retrieve users or a specific user by id
@app.route('/users', methods=['GET'])
def get_users():
    user_id = request.args.get('id')  # Retrieve 'id' from query parameters
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get column names in the results

    if user_id:
        # Query for a specific user if 'id' parameter is provided
        query = "SELECT id, username FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return jsonify(user)  # Return the specific user's data
        else:
            return jsonify({'error': 'User not found'}), 404  # Return 404 if the user is not found
    else:
        # Query to retrieve all users if no 'id' is provided
        query = "SELECT id, username FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(users)  # Return all users

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
