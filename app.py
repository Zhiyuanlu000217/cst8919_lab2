from flask import Flask, request
import logging
import os

app = Flask(__name__)

# --- Logging Configuration ---
log_directory = 'logs'
log_file_path = os.path.join(log_directory, 'app.log')

# Create the logs directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create a custom logger for our application
app_logger = logging.getLogger('flask_login_app_logger')
app_logger.setLevel(logging.INFO) # Set the minimum level for our app's logs

# Create a file handler that writes log messages to app.log
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO) # Minimum level for file output

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to our custom logger
app_logger.addHandler(file_handler)

# Disable Flask's default logger to prevent redundant output
logging.getLogger('werkzeug').handlers = []

# Basic user for demonstration (same as before)
VALID_USERNAME = "user"
VALID_PASSWORD = "password"

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            # Use our custom logger
            app_logger.warning(f"Failed login attempt: Missing credentials from IP: {request.remote_addr}")
            return {"message": "Missing username or password"}, 400

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            # Use our custom logger
            app_logger.info(f"Successful login attempt for username: {username} from IP: {request.remote_addr}")
            return {"message": "Login successful!"}, 200
        else:
            # Use our custom logger
            app_logger.warning(f"Failed login attempt for username: {username} (Incorrect credentials) from IP: {request.remote_addr}")
            return {"message": "Invalid username or password"}, 401
    return {"message": "Method Not Allowed"}, 405

if __name__ == '__main__':
    # When debug=True, Flask's reloader and debugger can still produce console output.
    # The file logging is separate and will be clean.
    app.run(debug=True)