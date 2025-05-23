
import sqlite3

DB_PATH = "mega_monetky_bot.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_user(chat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (chat_id TEXT PRIMARY KEY, clicks INTEGER, referrals INTEGER, balance INTEGER, last_bonus INTEGER, level INTEGER, game_active INTEGER, game_number INTEGER)")
    cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT INTO users VALUES (?, 0, 0, 0, 0, 1, 0, 0)", (chat_id,))
        conn.commit()
        row = (chat_id, 0, 0, 0, 0, 1, 0, 0)
    user = {
        "chat_id": row[0],
        "clicks": row[1],
        "referrals": row[2],
        "balance": row[3],
        "last_bonus": row[4],
        "level": row[5],
        "game_state": {"active": bool(row[6]), "number": row[7]}
    }
    conn.close()
    return user

def save_user(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET clicks=?, referrals=?, balance=?, last_bonus=?, level=?, game_active=?, game_number=? WHERE chat_id=?",
        (user["clicks"], user["referrals"], user["balance"], user["last_bonus"], user["level"],
         int(user["game_state"]["active"]), user["game_state"]["number"], user["chat_id"]))
    conn.commit()
    conn.close()
