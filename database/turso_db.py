import os
import libsql


def get_turso_connection():
    url = os.environ.get("TURSO_DATABASE_URL")
    token = os.environ.get("TURSO_AUTH_TOKEN")

    if not url or not token:
        raise RuntimeError(
            "TURSO_DATABASE_URL or TURSO_AUTH_TOKEN is missing"
        )

    conn = libsql.connect(
        database=url,
        auth_token=token
    )
    conn.row_factory = libsql.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
