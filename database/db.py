
import os
import libsql

from database.turso_db import get_turso_connection


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")


def get_connection():
    """Return a connection to the Turso database."""
    return get_turso_connection()


def column_exists(conn, table_name, column_name):
    # Table and column names below are internal application identifiers.
    if not table_name.replace("_", "").isalnum():
        raise ValueError("Invalid table name")

    cursor = conn.execute(
        f'PRAGMA table_info("{table_name}")'
    )
    return any(row["name"] == column_name for row in cursor.fetchall())


def add_column_if_missing(
    conn, table_name, column_name, column_definition
):
    allowed = {
        ("jobs", "post_date"),
        ("jobs", "responsibilities"),
    }

    if (table_name, column_name) not in allowed:
        raise ValueError("Unsupported migration")

    if column_exists(conn, table_name, column_name):
        return False

    conn.execute(
        f'ALTER TABLE "{table_name}" '
        f'ADD COLUMN "{column_name}" {column_definition}'
    )
    return True


def migrate_jobs_table(conn):
    changes = []

    if add_column_if_missing(
        conn, "jobs", "post_date", "TEXT"
    ):
        changes.append("Added jobs.post_date")

    if add_column_if_missing(
        conn, "jobs", "responsibilities", "TEXT"
    ):
        changes.append("Added jobs.responsibilities")

    return changes


def run_migrations(conn):
    return migrate_jobs_table(conn)


def create_database():
    """Check the existing Turso schema and apply safe migrations."""
    conn = get_connection()

    try:
        # This checks connectivity; it does not create a local SQLite DB.
        conn.execute("SELECT 1").fetchone()

        changes = run_migrations(conn)
        conn.commit()

        if changes:
            print("Database migrations:", ", ".join(changes))
        else:
            print("Turso database connected; no migrations needed.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
