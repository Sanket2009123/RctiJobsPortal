from flask import Flask
import os

import config
from database.db import create_database
from routes import register_routes
from authlib.integrations.flask_client import OAuth
from flask import jsonify
import firebase_admin
from firebase_admin import auth
from firebase.firebase_config import *
app = Flask(__name__)
app.config.from_object(config)

# ==========================
# Free Email / Gmail SMTP
# ==========================
# Set these values as environment variables on your PC.
# Do NOT put your Gmail password directly in this file.
app.config["SMTP_HOST"] = os.getenv("SMTP_HOST", "smtp.gmail.com")
app.config["SMTP_PORT"] = int(os.getenv("SMTP_PORT", "587"))
app.config["SMTP_USERNAME"] = os.getenv("SMTP_USERNAME", "")
app.config["SMTP_PASSWORD"] = os.getenv("SMTP_PASSWORD", "")
app.config["MAIL_FROM"] = os.getenv("MAIL_FROM", "")
app.config["PORTAL_BASE_URL"] = os.getenv(
    "PORTAL_BASE_URL",
    "http://127.0.0.1:5000"
)



# ==========================
# Secret Key
# ==========================
app.secret_key = app.config["SECRET_KEY"]
oauth = OAuth(app)

# google = oauth.register(
#     name="google",
#     client_id=app.config["GOOGLE_CLIENT_ID"],
#     client_secret=app.config["GOOGLE_CLIENT_SECRET"],
#     server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
#     client_kwargs={
#         "scope": "openid email profile"
#     }
# )
# ==========================
# Upload Folders
# ==========================
app.config["PROFILE_FOLDER"] = os.path.join(app.root_path, "static", "uploads", "profile")
app.config["RESUME_FOLDER"] = os.path.join(app.root_path, "static", "uploads", "resume")

os.makedirs(app.config["PROFILE_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESUME_FOLDER"], exist_ok=True)

# ==========================
# Create Database
# ==========================
create_database()

# ==========================
# Register All Routes
# ==========================
register_routes(app)
# ==========================
# Disable Browser Cache
# ==========================
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
# ==========================
# Run App
# ==========================
if __name__ == "__main__":
    app.run()