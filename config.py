import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# ==========================
# Flask Security
# ==========================

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this-key")


# ==========================
# Database
# ==========================

DATABASE = os.getenv("DATABASE", "database.db")


# ==========================
# Upload Folders
# ==========================

UPLOAD_FOLDER = "static/uploads"
COMPANY_LOGO_FOLDER = "static/uploads/company_logos"


# ==========================
# Gmail SMTP Configuration
# ==========================

EMAIL_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("SMTP_PORT", "587"))

EMAIL_ADDRESS = os.getenv("SMTP_USERNAME", "")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD", "")


# ==========================
# Portal Base URL
# ==========================

PORTAL_BASE_URL = os.getenv(
    "PORTAL_BASE_URL",
    "http://127.0.0.1:5000"
)