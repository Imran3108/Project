import sqlite3
import datetime

DB_NAME = "vulnerability_results.db"

def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pr_number INTEGER,
            filename TEXT,
            status TEXT,
            severity TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized.")

def save_result(pr_number, filename, status, severity):
    """Saves a vulnerability scan result to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO results (pr_number, filename, status, severity, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (pr_number, filename, status, severity, timestamp))
    conn.commit()
    conn.close()
    print(f"Saved result for PR #{pr_number} - {filename}")

def get_all_results():
    """Retrieves all results from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
