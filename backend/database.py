import sqlite3

def init_db():
    conn = sqlite3.connect("cost.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cost_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        current_cost REAL,
        predicted_cost REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_cost(current, predicted):
    conn = sqlite3.connect("cost.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO cost_history (current_cost, predicted_cost)
    VALUES (?, ?)
    """, (current, predicted))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect("cost.db")
    cursor = conn.cursor()

    cursor.execute("SELECT current_cost, predicted_cost, timestamp FROM cost_history ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()

    conn.close()
    return data