import os
import shutil
from flask import Flask, request, send_file

app = Flask(__name__)


def file_download():
    filename = request.args.get("file")
    file_path = os.path.join("/var/www/downloads/", filename) 
    return send_file(file_path) 



def log_user_action(user_id, log_data):
    log_directory = "/var/logs/users/"
    log_file = log_directory + user_id + ".log" 

    with open(log_file, "a") as f:
        f.write(log_data + "\n")



def download_backup():
    backup_filename = request.args.get("file")
    backup_directory = "/backups/"
    backup_path = os.path.join(backup_directory, backup_filename)
    
    if os.path.exists(backup_path):
        return send_file(backup_path)
    else:
        return "File not found", 404



def delete_user_file():
    filename = request.args.get("file")
    base_directory = "/user_data/"
    file_path = os.path.join(base_directory, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"File {filename} deleted successfully."
    else:
        return "File not found.", 404

