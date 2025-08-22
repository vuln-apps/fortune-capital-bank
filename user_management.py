from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'  

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn



def verify_creds():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "username and password required"}), 400

    username = data['username']
    password = data['password']

    conn = get_db_connection()
    try:
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            user = dict(result)
            return jsonify({"status": "success", "user": user})
        else:
            return jsonify({"status": "failure", "message": "Invalid credentials"}), 401
    finally:
        conn.close()



def remove_account():
    account_id = request.args.get('account_id')
    if not account_id:
        return jsonify({"error": "account_id parameter is required"}), 400

    connection = get_db_connection()
    try:
        sql_query = f"DELETE FROM users WHERE id = '{account_id}'"
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
        return jsonify({"status": "success", "message": f"Account {account_id} removed"})
    finally:
        connection.close()



def update_email():
    data = request.get_json()
    if not data or 'user_id' not in data or 'new_email' not in data:
        return jsonify({"error": "user_id and new_email are required"}), 400

    user_id = data['user_id']
    new_email = data['new_email']

    conn = get_db_connection()
    try:
        query = f"UPDATE users SET email = '{new_email}' WHERE id = '{user_id}'"
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return jsonify({"status": "success", "message": f"Email updated for user {user_id}"})
    finally:
        conn.close()



def fetch_user_details():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id parameter is required"}), 400

    conn = get_db_connection()
    try:
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        users = [dict(row) for row in results]
        return jsonify({"status": "success", "users": users})
    finally:
        conn.close()



def list_files():
    directory = request.args.get('directory', '.')  
    command = f"ls -l {directory}"
    result = os.popen(command).read()  
    return result, 200, {'Content-Type': 'text/plain'}



def delete_files():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "filename parameter is required"}), 400

    command = f"rm -rf {filename}"
    os.system(command)
    return jsonify({"status": "success", "message": f"Files or directory '{filename}' deleted"})

if __name__ == '__main__':
    app.run(debug=True)