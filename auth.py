import requests
import jwt
import datetime
from flask import abort, request, current_app
from functools import wraps
from config import db

# --- SWAGGER SECURITY FUNCTION ---
# This function is called automatically by Swagger/Connexion
def decode_token(token):
    try:
        # Decode the token using your Secret Key
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return data  # Returns {'User_ID': 1, 'Role': 'Admin', ...}
    except:
        return None  # Triggers a 401 Unauthorized error automatically

# --- 1. TOKEN DECORATOR (Now checks for ADMIN Role) ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            abort(401, "Token is missing. Please login first.")

        try:
            # 2. Decode the token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['User_ID']
            current_user_role = data['Role'] # <--- Get the role
            
            # 3. ENFORCE ADMIN CHECK
            # If the user is NOT an Admin, they cannot perform this action.
            if current_user_role != 'Admin':
                abort(403, "Permission Denied: You must be an Administrator to perform this action.")

        except jwt.ExpiredSignatureError:
            abort(401, "Token has expired. Please login again.")
        except jwt.InvalidTokenError:
            abort(401, "Token is invalid.")
        except Exception as e:
            abort(500, f"Token error: {str(e)}")

        # 4. Pass the User ID to the function
        return f(current_user_id, *args, **kwargs)

    return decorated

# --- 2. LOGIN FUNCTION ---
def login():
    """
    POST /login
    """
    try:
        credentials = request.get_json()
        email = credentials.get("email")
        password = credentials.get("password")
        
        auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
        response = requests.post(auth_url, json={"email": email, "password": password})
        
        print(f"Uni API Status: {response.status_code}")
        
        if response.status_code == 200:
            json_data = response.json()

            # CHECK: Handle the specific List format ["Verified", "True"]
            is_verified = False
            if isinstance(json_data, list) and len(json_data) == 2:
                if json_data[0] == "Verified" and json_data[1] == "True":
                    is_verified = True
            
            if is_verified:
                # Auth successful! Find local user
                sql = "SELECT User_ID, Username, Role FROM CW2.[USER] WHERE Email = :email"
                result = db.session.execute(db.text(sql), {"email": email}).mappings().one_or_none()
                
                if result:
                    user_data = dict(result)
                    
                    # Generate Token (Includes Role!)
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
                abort(401, "Invalid email or password (University API returned False)")
        else:
            abort(401, "Invalid request to Auth API")
            
    except Exception as e:
        print(f"Login Error: {e}") 
        abort(500, f"Authentication error: {str(e)}")