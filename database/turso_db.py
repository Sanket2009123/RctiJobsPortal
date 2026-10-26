import os
import libsql

def get_turso_connection():
    url = os.environ["TURSO_DATABASE_URL"]
    token = os.environ["TURSO_AUTH_TOKEN"]

    return libsql.connect(
        database=url,
        auth_token=token
    )
