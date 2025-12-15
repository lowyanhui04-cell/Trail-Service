import requests
import jwt
import datetime
from flask import abort, request, current_app
from functools import wraps
from config import db

def decode_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return data
    except:
        return None

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
            current_user_role = data['Role']

            if current_user_role != 'Admin':
                abort(403, "Permission Denied: You must be an Administrator to perform this action.")

        except jwt.ExpiredSignatureError:
            abort(401, "Token has expired. Please login again.")
        except jwt.InvalidTokenError:
            abort(401, "Token is invalid.")
        except Exception as e:
            abort(500, f"Token error: {str(e)}")

        return f(current_user_id, *args, **kwargs)
    return decorated

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

            is_verified = False
            if isinstance(json_data, list) and len(json_data) == 2:
                if json_data[0] == "Verified" and json_data[1] == "True":
                    is_verified = True
            
            if is_verified:
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
                abort(401, "Invalid email or password (University API returned False)")
        else:
            abort(401, "Invalid request to Auth API")
            
    except Exception as e:
        print(f"Login Error: {e}") 
        abort(500, f"Authentication error: {str(e)}")