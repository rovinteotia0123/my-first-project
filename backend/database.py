import sqlite3

DB_NAME = "cost.db"


# ------------------ INIT DATABASE ------------------
def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # Cost history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cost_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        current_cost REAL,
        predicted_cost REAL,
        timestamp DATETIME DEFAULT (datetime('now','localtime'))
    )
    """)

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE
    )
    """)

    conn.commit()

    conn.close()


# ------------------ SAVE COST ------------------
def save_cost(current, predicted):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO cost_history (current_cost, predicted_cost)
    VALUES (?, ?)
    """, (current, predicted))

    conn.commit()

    conn.close()


# ------------------ SAVE USER ------------------
def save_user(email):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (email) VALUES (?)",
        (email,)
    )

    conn.commit()

    conn.close()


# ------------------ GET HISTORY ------------------
def get_history():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT current_cost, predicted_cost, timestamp
    FROM cost_history
    ORDER BY timestamp DESC
    LIMIT 10
    """)

    data = cursor.fetchall()

    conn.close()

    return [
        (row[0], row[1], str(row[2]))
        for row in data
    ]


# ------------------ OPTIONAL CLEAR ------------------
def clear_history():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM cost_history")

    conn.commit()

    conn.close()