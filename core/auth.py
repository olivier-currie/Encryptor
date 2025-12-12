
import os
from db.database import get_connection
import sqlite3
import smtplib
from email.message import EmailMessage
import base64
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
    message = EmailMessage()
    message.set_content(f"Your verification code is: {code}")
    message['Subject'] = "Confirm your account e-mail"
    message['From'] = "encrypteur@gmail.com"
    message['To'] = to_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("encrypteur@gmail.com", "xwmb afmh sjlg vqnp")
        smtp.send_message(message)

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
    

