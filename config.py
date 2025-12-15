<<<<<<< HEAD
import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

# UPDATED FOR YOUR SPECIFIC DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=MAL2018_Information_Management_Retrieval;"  # <-- The name from your screenshot
    "UID=SA;"
    "PWD=C0mp2001!;"               # Assuming you used the standard password
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super_secret_key_for_assignment_cw2"

db = SQLAlchemy(app)
=======
import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

# UPDATED FOR YOUR SPECIFIC DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=MAL2018_Information_Management_Retrieval;"  # <-- The name from your screenshot
    "UID=SA;"
    "PWD=C0mp2001!;"               # Assuming you used the standard password
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
>>>>>>> e2889fc1841252d7c44d92ac0068773bc7bfc1eb
ma = Marshmallow(app)