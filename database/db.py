import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")


def get_connection():
    """Create and return a SQLite connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def cleanup_sequence_if_empty(conn, table_name):
    """Remove sqlite_sequence entry only when the table is empty."""

    if not table_name.replace("_", "").isalnum():
        raise ValueError("Invalid table name.")

    cursor = conn.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')

    row = cursor.fetchone()
    count = row[0] if row else 0

    if count == 0:
        cursor.execute(
            "DELETE FROM sqlite_sequence WHERE name = ?",
            (table_name,)
        )


def column_exists(conn, table_name, column_name):
    """Check whether a SQLite table already contains a column."""

    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info("{table_name}")')

    return any(
        row["name"] == column_name
        for row in cursor.fetchall()
    )


def add_column_if_missing(
    conn,
    table_name,
    column_name,
    column_definition
):
    """Add a column only when it does not already exist."""

    if not table_name.replace("_", "").isalnum():
        raise ValueError("Invalid table name.")

    if not column_name.replace("_", "").isalnum():
        raise ValueError("Invalid column name.")

    if column_exists(conn, table_name, column_name):
        return False

    cursor = conn.cursor()

    sql = (
        f'ALTER TABLE "{table_name}" '
        f'ADD COLUMN "{column_name}" {column_definition}'
    )

    cursor.execute(sql)
    return True


def migrate_jobs_table(conn):
    """
    Add the columns required by the current job-posting system.

    Existing jobs and other database data are preserved.
    """

    changes = []

    if add_column_if_missing(
        conn,
        "jobs",
        "post_date",
        "TEXT"
    ):
        changes.append("jobs.post_date")

    if add_column_if_missing(
        conn,
        "jobs",
        "responsibilities",
        "TEXT"
    ):
        changes.append("jobs.responsibilities")

    return changes


def run_migrations(conn):
    """Run all application database migrations."""
    return migrate_jobs_table(conn)


def create_database():
    """
    Create the database if needed and always run migrations.

    Existing database records are never deleted.
    """

    database_exists = os.path.exists(DATABASE)
    conn = get_connection()

    try:
        cursor = conn.cursor()

        # ------------------------------------------------------
        # Create database for the first time
        # ------------------------------------------------------

        if not database_exists:

            if not os.path.exists(SCHEMA_FILE):
                raise FileNotFoundError(
                    f"Schema file not found: {SCHEMA_FILE}"
                )

            with open(
                SCHEMA_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                conn.executescript(file.read())

        # ------------------------------------------------------
        # Run migrations on both new and existing databases
        # ------------------------------------------------------

        changes = run_migrations(conn)

        # ------------------------------------------------------
        # Default admin
        # ------------------------------------------------------

        cursor.execute(
            "SELECT 1 FROM admins WHERE email = ?",
            ("admin@gmail.com",)
        )

        if cursor.fetchone() is None:
            cursor.execute(
                """
                INSERT INTO admins
                (
                    name,
                    email,
                    password
                )
                VALUES (?, ?, ?)
                """,
                (
                    "Administrator",
                    "admin@gmail.com",
                    "Admin@2026"
                )
            )

        conn.commit()

        if changes:
            print("Database migration completed.")

            for change in changes:
                print(f"  Added: {change}")

        elif database_exists:
            print("Database checked. No new migration required.")

        else:
            print("Database created successfully.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    create_database()