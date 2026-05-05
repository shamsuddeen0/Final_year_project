import os
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

from crypto_manager import crypto_manager
from honeyword_generator import honeyword_generator
from alert_system import alert_system

app = FastAPI(title="Honeyword IDS")

# Database connection configuration
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "honeyword_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

def get_db_connection():
    conn = psycopg2.connect(**DB_PARAMS)
    return conn

# Models
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # 1. Hash real password
        hashed_pw = crypto_manager.hash_password(user_data.password)

        # 2. Insert user
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id",
            (user_data.username, hashed_pw)
        )
        user_id = cur.fetchone()['id']

        # 3. Generate and encrypt honeywords (19 decoys)
        honeywords = honeyword_generator.generate(user_data.password, count=19)
        for word in honeywords:
            encrypted_word = crypto_manager.encrypt_honeyword(word)
            cur.execute(
                "INSERT INTO honeywords (user_id, encrypted_word) VALUES (%s, %s)",
                (user_id, encrypted_word)
            )

        conn.commit()
        return {"message": "User registered successfully"}

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/login")
async def login(user_data: UserLogin):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # 1. Fetch user
        cur.execute("SELECT * FROM users WHERE username = %s", (user_data.username,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # 2. Check real password (Argon2id)
        if crypto_manager.verify_password(user['password_hash'], user_data.password):
            return {"message": "Login successful", "role": "user"}

        # 3. Check honeywords (AES)
        cur.execute("SELECT encrypted_word FROM honeywords WHERE user_id = %s", (user['id'],))
        honeywords = cur.fetchall()

        for hw in honeywords:
            decrypted_word = crypto_manager.decrypt_honeyword(hw['encrypted_word'])
            if decrypted_word == user_data.password:
                # CRITICAL: Honeyword hit!
                # Use professional alert system
                alert_system.trigger_alert(
                    username=user['username'],
                    honeyword_used=decrypted_word,
                    ip_address="Unknown/Local" # In real FastAPI, use request.client.host
                )
                # We grant access to avoid tipping off the attacker
                return {"message": "Login successful", "role": "user"}

        # If neither matches
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
