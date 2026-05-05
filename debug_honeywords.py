import psycopg2
from psycopg2.extras import RealDictCursor
from crypto_manager import crypto_manager

DB_PARAMS = {
    "dbname": "honeyword_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}

def get_actual_honeywords(username):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Find user id
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if not user:
            print(f"User {username} not found!")
            return

        # Get encrypted honeywords
        cur.execute("SELECT encrypted_word FROM honeywords WHERE user_id = %s", (user['id'],))
        rows = cur.fetchall()

        print(f"\n--- Honeywords for {username} ---")
        for i, row in enumerate(rows):
            decrypted = crypto_manager.decrypt_honeyword(row['encrypted_word'])
            print(f"Honeyword #{i+1}: {decrypted}")
        print("---------------------------------\n")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # We'll try 'testuser' as the default
    get_actual_honeywords("testuser")
