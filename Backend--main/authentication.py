from flask import Blueprint, jsonify, request
from supabase import create_client
from datetime import datetime, timedelta
from secrets import token_urlsafe
import bcrypt
import os
from dotenv import load_dotenv
import logging
from functools import wraps

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Initialize Supabase client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

# Add debug logging
logging.debug(f"SUPABASE_URL: {supabase_url}")
logging.debug(f"SUPABASE_KEY length: {len(supabase_key or '')}")

if not supabase_url or not supabase_key:
    raise ValueError("Missing required environment variables SUPABASE_URL or SUPABASE_KEY")

# Make sure the URL starts with https:// and ends with .supabase.co
if not supabase_url.startswith('https://') or not supabase_url.endswith('.supabase.co'):
    raise ValueError("Invalid Supabase URL format. It should start with 'https://' and end with '.supabase.co'")

print(f"Using Supabase URL: '{supabase_url}'")

# Add this before create_client
print(f"URL characters: {[ord(c) for c in supabase_url]}")

supabase = create_client(supabase_url, supabase_key)

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')  # Changed from '/api' to '/auth'

# Store reset tokens with expiry (in memory - will be cleared when server restarts)
reset_tokens = {}

def hash_password(password):
    # Convert the password to bytes if it's not already
    if isinstance(password, str):
        password = password.encode('utf-8')
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    # Return the hashed password as a string
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    try:
        # Convert passwords to bytes if they're not already
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        # Verify the password
        return bcrypt.checkpw(password, hashed_password)
    except Exception as e:
        logging.error(f"Password verification error: {str(e)}")
        return False

@auth_bp.route("/home", methods=['GET'])
def return_home():
    logging.info("Home route accessed")  # Log an info message
    return jsonify({
        'message': "Hello World!"
    })

@auth_bp.route("/signup", methods=['POST'])
def signup():
    try:
        data = request.get_json()
        logging.debug(f"Signup request data: {data}")
        
        # Basic validation
        required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
        if not all(key in data for key in required_fields):
            logging.warning("Missing required fields in signup request")
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            # Check if email already exists
            existing_email = supabase.table('users').select('*').eq('email', data['email']).execute()
            if len(existing_email.data) > 0:
                logging.warning(f"Email already registered: {data['email']}")
                return jsonify({'error': 'This email is already registered'}), 400
            
            # Check if username already exists
            existing_username = supabase.table('users').select('*').eq('username', data['username']).execute()
            if len(existing_username.data) > 0:
                logging.warning(f"Username already taken: {data['username']}")
                return jsonify({'error': 'This username is already taken'}), 400
            
            # Hash the password
            hashed_password = hash_password(data['password'])
            
            # Create user object without id (let Supabase auto-generate it)
            new_user_data = {
                'first_name': data['firstName'],
                'last_name': data['lastName'],
                'username': data['username'],
                'email': data['email'],
                'password': hashed_password,
                'role': 'public',
                'created_at': datetime.now().isoformat()  # Add creation timestamp
            }
            
            # Insert new user
            result = supabase.table('users').insert(new_user_data).execute()
            
            if not result.data:
                raise Exception("Failed to create user")
                
            logging.info(f"New user registered: {data['email']}")
            
            # Return success response without sensitive data
            return jsonify({
                'message': 'User registered successfully',
                'user': {
                    'firstName': data['firstName'],
                    'lastName': data['lastName'],
                    'username': data['username'],
                    'email': data['email'],
                    'role': 'public'
                }
            }), 201
            
        except Exception as db_error:
            logging.error(f"Database error during signup: {str(db_error)}", exc_info=True)
            return jsonify({'error': 'An error occurred during registration. Please try again.', 'details': str(db_error)}), 500
            
    except Exception as e:
        logging.critical(f"Server error during signup: {str(e)}", exc_info=True)
        return jsonify({'error': 'Server error. Please try again later.', 'details': str(e)}), 500

@auth_bp.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        logging.debug(f"Login attempt received with data: {data}")  # Added debug logging
        
        if not all(key in data for key in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400
        
        try:
            # Find user by email
            logging.debug(f"Querying database for email: {data['email']}")  # Added debug logging
            result = supabase.table('users').select('*').eq('email', data['email']).execute()
            logging.debug(f"Database query result: {result.data}")  # Added debug logging
            
            if not result.data:
                return jsonify({'error': 'Invalid email or password'}), 401
            
            user = result.data[0]
            stored_password = user.get('password', '')
            
            logging.debug(f"Attempting password verification for user: {data['email']}")  # Added debug logging
            # Verify password
            if verify_password(data['password'], stored_password):
                logging.info(f"Successful login for: {data['email']}")
                return jsonify({
                    'message': 'Login successful',
                    'user': {
                        'firstName': user['first_name'],
                        'lastName': user['last_name'],
                        'username': user['username'],
                        'email': user['email'],
                        'role': user['role']
                    }
                })
            
            logging.warning(f"Password verification failed for: {data['email']}")  # Added debug logging
            return jsonify({'error': 'Invalid email or password'}), 401
                
        except Exception as db_error:
            logging.error(f"Database error during login: {str(db_error)}")
            return jsonify({'error': 'Login failed. Please try again.'}), 500
            
    except Exception as e:
        logging.error(f"Server error during login: {str(e)}")
        return jsonify({'error': 'Server error. Please try again later.'}), 500

@auth_bp.route("/request-reset", methods=['POST'])
def request_reset():
    try:
        data = request.get_json()
        email = data.get('email')
        logging.debug(f"Password reset request for email: {email}")  # Log the request data
        
        if not email:
            logging.warning("Email is required for password reset")  # Log a warning
            return jsonify({'error': 'Email is required'}), 400
        
        try:
            # Check if user exists
            result = supabase.table('users').select('*').eq('email', email).execute()
            
            if len(result.data) == 0:
                logging.warning(f"Email not found: {email}")  # Log a warning
                return jsonify({'message': 'If the email exists, a reset token will be sent'}), 200
            
            # Generate reset token
            reset_token = token_urlsafe(32)
            logging.debug(f"Generated reset token: {reset_token} for email: {email}")  # Log a debug message
            
            # Store token with expiry (1 hour)
            reset_tokens[reset_token] = {
                'email': email,
                'expiry': datetime.now() + timedelta(hours=1)
            }
            
            # Return the token directly
            return jsonify({
                'message': 'Password reset token generated',
                'token': reset_token
            }), 200
            
        except Exception as db_error:
            logging.error(f"Database error during password reset request: {str(db_error)}", exc_info=True)  # Log the error with traceback
            return jsonify({'error': 'Failed to process reset request', 'details': str(db_error)}), 500
            
    except Exception as e:
        logging.critical(f"Server error during password reset request: {str(e)}", exc_info=True)  # Log the critical error with traceback
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@auth_bp.route("/reset-password", methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        email = data.get('email')
        new_password = data.get('newPassword')
        logging.debug(f"Password reset request for email: {email}")  # Log the request data
        
        if not email or not new_password:
            logging.warning("Email and new password are required for password reset")  # Log a warning
            return jsonify({'error': 'Email and new password are required'}), 400
        
        try:
            # Check if user exists
            result = supabase.table('users').select('*').eq('email', email).execute()
            
            if len(result.data) == 0:
                logging.warning(f"Email not found: {email}")  # Log a warning
                return jsonify({'error': 'Email not found'}), 404
            
            # Hash the new password
            hashed_password = hash_password(new_password)
            logging.debug("New password hashed successfully")  # Log a debug message
            
            # Update password in database
            result = supabase.table('users').update({
                'password': hashed_password
            }).eq('email', email).execute()
            logging.info(f"Password updated for email: {email}")  # Log an info message
            
            return jsonify({'message': 'Password updated successfully'}), 200
            
        except Exception as db_error:
            logging.error(f"Database error during password reset: {str(db_error)}", exc_info=True)  # Log the error with traceback
            return jsonify({'error': 'Failed to update password', 'details': str(db_error)}), 500
            
    except Exception as e:
        logging.critical(f"Server error during password reset: {str(e)}", exc_info=True)  # Log the critical error with traceback
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

def init_routes(bp):
    bp.route("/home", methods=['GET'])(return_home)
    bp.route("/signup", methods=['POST'])(signup)
    bp.route("/login", methods=['POST'])(login)
    bp.route("/request-reset", methods=['POST'])(request_reset)
    bp.route("/reset-password", methods=['POST'])(reset_password)