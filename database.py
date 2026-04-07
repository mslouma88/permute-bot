import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)

cursor = conn.cursor()

def init_db():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        discord_id TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shifts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        agent TEXT,
        shift TEXT
    )
    """)

    conn.commit()

def add_agent(name, discord_id):

    cursor.execute(
        "INSERT INTO agents(name,discord_id) VALUES (?,?)",
        (name, discord_id)
    )

    conn.commit()

def get_agents():

    cursor.execute("SELECT * FROM agents")

    return cursor.fetchall()

def add_shift(date, agent, shift):

    cursor.execute(
        "INSERT INTO shifts(date,agent,shift) VALUES (?,?,?)",
        (date, agent, shift)
    )

    conn.commit()

def get_shift(agent, date):

    cursor.execute(
        "SELECT shift FROM shifts WHERE agent=? AND date=?",
        (agent, date)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return None