import sqlite3
from datetime import datetime

DATABASE = "bmi_history.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the BMI history table if it does not already exist."""
    connection = None

    try:
        connection = get_connection()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                height REAL NOT NULL,
                weight REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)

        connection.commit()

    except sqlite3.Error as error:
        print("Database initialization error:", error)

    finally:
        if connection:
            connection.close()


def save_bmi_record(
    user_name,
    age,
    gender,
    height,
    weight,
    bmi,
    category
):
    """Save a BMI calculation to the database."""

    connection = None

    try:
        connection = get_connection()

        connection.execute("""
            INSERT INTO bmi_records
            (
                user_name,
                age,
                gender,
                height,
                weight,
                bmi,
                category,
                recorded_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_name,
            age,
            gender,
            height,
            weight,
            bmi,
            category,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        connection.commit()
        return True

    except sqlite3.Error as error:
        print("Error saving BMI record:", error)
        return False

    finally:
        if connection:
            connection.close()


def get_user_records(user_name):
    """Return all BMI records for a particular user."""

    connection = None

    try:
        connection = get_connection()

        cursor = connection.execute("""
            SELECT *
            FROM bmi_records
            WHERE user_name = ?
            ORDER BY id DESC
        """, (user_name,))

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Error retrieving records:", error)
        return []

    finally:
        if connection:
            connection.close()


def get_all_records():
    """Return all BMI records."""

    connection = None

    try:
        connection = get_connection()

        cursor = connection.execute("""
            SELECT *
            FROM bmi_records
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Error retrieving all records:", error)
        return []

    finally:
        if connection:
            connection.close()