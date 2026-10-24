import os
import json
import firebase_admin
from firebase_admin import credentials


# ==========================================
# Firebase Service Account Configuration
# ==========================================

def get_firebase_credential():
    """
    Production:
        Reads Firebase service-account JSON
        from FIREBASE_SERVICE_ACCOUNT environment variable.

    Local development:
        Falls back to serviceAccountKey.json.
    """

    firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")

    # ------------------------------------------
    # Production / Environment Variable
    # ------------------------------------------
    if firebase_json:
        if os.path.exists(firebase_json):
            return credentials.Certificate(firebase_json)
        try:
            service_account_info = json.loads(firebase_json)
            return credentials.Certificate(service_account_info)
        except json.JSONDecodeError:
            pass

    # ------------------------------------------
    # Local Development
    # ------------------------------------------
    base_dir = os.path.dirname(os.path.abspath(__file__))

    service_account_path = os.path.join(
        base_dir,
        "serviceAccountKey.json"
    )

    if not os.path.exists(service_account_path):
        raise FileNotFoundError(
            "Firebase service account credentials not found. "
            "Set FIREBASE_SERVICE_ACCOUNT environment variable "
            "or provide firebase/serviceAccountKey.json locally."
        )

    return credentials.Certificate(service_account_path)


# ==========================================
# Initialize Firebase Only Once
# ==========================================

try:
    firebase_admin.get_app()

except ValueError:
    cred = get_firebase_credential()
    firebase_admin.initialize_app(cred)