<<<<<<< HEAD
import requests
import jwt
import datetime
from flask import abort, request, current_app
from functools import wraps
from config import db

# ==========================================
# 1. TOKEN DECORATOR
# ==========================================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            abort(401, "Token is missing. Please login first.")

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['User_ID']
        except Exception as e:
            abort(401, "Token is invalid or expired.")

        return f(current_user_id, *args, **kwargs)

    return decorated

# ==========================================
# 2. LOGIN FUNCTION (Fixed Logic)
# ==========================================
def login(**kwargs):
    """
    POST /login
    Accepts {email, password}
    """
    credentials = request.get_json()
    email = credentials.get("email")
    password = credentials.get("password")

    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
    
    try:
        response = requests.post(auth_url, json={"email": email, "password": password})
        
        # 1. Check Status Code
        if response.status_code == 200:
            
            # === THE FIX IS HERE ===
            # The University API returns 200 OK even for wrong passwords.
            # But the BODY contains "Verified: false" or just "false".
            # We must catch this!
            try:
                data = response.json()
                
                # If the API returns literally 'False' (boolean)
                if data is False:
                    abort(401, "Invalid password (Verified: False)")
                
                # If the API returns ["Verified", False] (list)
                if isinstance(data, list) and len(data) >= 2 and data[1] is False:
                    abort(401, "Invalid password (Verified: False)")
                    
            except Exception:
                # If it's not JSON, we assume it's okay for now
                pass
            # =======================

            # If we get here, the password is TRULY correct.
            sql = "SELECT User_ID, Username, Role FROM CW2.[USER] WHERE Email = :email"
            result = db.session.execute(db.text(sql), {"email": email}).mappings().one_or_none()
            
            if result:
                user_data = dict(result)
                token = jwt.encode({
                    'User_ID': user_data['User_ID'],
                    'Role': user_data['Role'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, current_app.config['SECRET_KEY'], algorithm="HS256")

                return {
                    "token": token,
                    "user": user_data
                }, 200
            else:
                abort(401, "Login successful, but user not found in local CW2 database.")
        else:
            abort(401, "Invalid email or password")
            
    except Exception as e:
        # If we aborted above (401), re-raise it so Swagger sees it
        if "401" in str(e):
            abort(401, str(e))
=======
import requests
from flask import abort, request  # <--- CHANGED: Added 'request'
from config import db
from models import Trail

# This matches the local User table to get the ID
def login():  # <--- CHANGED: Removed 'credentials' from inside the brackets
    """
    POST /login
    Accepts {email, password}
    Returns {User_ID, Username, Role} if successful
    """
    # <--- CHANGED: We get the JSON body manually now
    credentials = request.get_json() 
    
    email = credentials.get("email")
    password = credentials.get("password")
    
    # 1. Authenticate against University API
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
    
    try:
        response = requests.post(auth_url, json={"email": email, "password": password})
        
        if response.status_code == 200:
            # Auth successful! Now find THIS user in OUR database
            # We use raw SQL to query your CW2.[USER] table
            sql = "SELECT User_ID, Username, Role FROM CW2.[USER] WHERE Email = :email"
            result = db.session.execute(db.text(sql), {"email": email}).mappings().one_or_none()
            
            if result:
                return dict(result), 200
            else:
                # User exists in Uni system but not in YOUR local database
                abort(401, "Login successful, but user not found in local CW2 database.")
        else:
            abort(401, "Invalid email or password")
            
    except Exception as e:
>>>>>>> e2889fc1841252d7c44d92ac0068773bc7bfc1eb
        abort(500, f"Authentication error: {str(e)}")