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
        abort(500, f"Authentication error: {str(e)}")