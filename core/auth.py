
import os
from db.database import get_connection
import sqlite3
import smtplib
from email.message import EmailMessage
import base64
import requests
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey

def hash_password(password):

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100_000,
    backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return base64.b64encode(salt + key).decode() 


def verify_password(username, password_attempt):
    stored = get_stored_pw(username)
    stored_bytes = base64.b64decode(stored)
    salt = stored_bytes[:16]
    stored_key = stored_bytes[16:]
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100_000,
    backend=default_backend()
    )
    try:
        kdf.verify(password_attempt.encode(), stored_key)
        return True
    except InvalidKey:
        return False

def get_stored_pw(username):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return row[0]
    finally:
        connection.close()

def create_user(username, email, password):
    connection = get_connection()
    cursor = connection.cursor()
    password_hash = hash_password(password)
    
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password_hash))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()

def send_email_verif(to_email, code):
    API_URL = "https://encryptorbackend-production.up.railway.app/send-verification"
    response = requests.post(API_URL, json={
        "to": to_email,
        "code": code
    })
    print("Status code:", response.status_code)
    print("Response:", response.text)
    if not response.ok:
        raise RuntimeError("Failed to send verification email")

def get_account_created(username):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT timestamp FROM users WHERE username = ? ",(username,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return row[0]
    finally:
        connection.close()

def get_email(username):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT email FROM users WHERE username = ? ",(username,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return row[0]
    finally:
        connection.close()

def delete_user(username):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE username = ? ",(username,))
        connection.commit()
    finally:
        connection.close()
    

