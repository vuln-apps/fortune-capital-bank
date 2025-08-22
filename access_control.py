from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)



def check_access():
    """
    Grants admin access if the user role is 'admin' or 'superuser'.
    It also contains a hidden bypass for the role 'bypass123'.
    """
    user_role = request.args.get('user_role', '')
    
    
    if user_role == "admin" or user_role == "superuser":
        return jsonify({"result": "Access granted: Admin privileges"})
    
    
    if user_role == "bypass123":
        return jsonify({"result": "Access granted: Backdoor admin privileges"})
    
    return jsonify({"result": "Access denied"})




def get_user_role():
    """
    Extracts user role from a cookie (passed as a query parameter)
    but does not verify its authenticity.
    """
    cookie = request.args.get('cookie', '')
    
    try:
        user_data = json.loads(cookie)
        role = user_data.get("role", "guest")
    except json.JSONDecodeError:
        role = "guest"
    
    return jsonify({"role": role})




def is_admin():
    """
    Grants admin access based on an API key using weak comparison.
    """
    api_key = request.args.get('api_key', '')
    admin_api_key = "secure_admin_key"
    
    if api_key == admin_api_key:
        return jsonify({"result": "Access granted: Admin"})
    
    return jsonify({"result": "Access denied"})




def elevate_privileges():
    """
    Changes the user role based on provided JSON input but lacks proper validation.
    """
    data = request.get_json(silent=True)
    if not data or "user_input" not in data:
        return jsonify({"error": "user_input not provided"}), 400

    user_input = data["user_input"]
    user_roles = ["user", "moderator", "admin"]

    if user_input in user_roles:
        result = f"Role changed to {user_input}"
    else:
        result = f"Role changed to {user_input} (unchecked input!)"

    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)