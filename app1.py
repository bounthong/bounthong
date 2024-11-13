from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'apis.com.la',       # Update with your database host
    'user': 'admin',     # Update with your database username
    'password': 'Sql_admin@#2024', # Update with your database password
    'database': 'bt'
}

# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# GET endpoint to retrieve users
@app.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get column names in the results
    query = "SELECT id, username FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
