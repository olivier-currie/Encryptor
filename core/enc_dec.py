from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
import os
from db.database import get_connection

def derive_key_iv(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=48,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key_iv = kdf.derive(password.encode())
    return key_iv[:32], key_iv[32:]

def encrypt(filepath, outpath, password):
    with open(filepath, 'rb') as f:
        data = f.read()

    salt = os.urandom(16)
    key, iv = derive_key_iv(password, salt)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    with open(outpath, 'wb') as f:
        f.write(salt + encrypted)

def decrypt(filepath, outpath, password):
    with open(filepath, 'rb') as f:
        data = f.read()

    salt = data[:16]
    encrypted = data[16:]

    key, iv = derive_key_iv(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    with open(outpath, 'wb') as f:
        f.write(decrypted)

def add_history(username, filename, action):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO history (username, filename, action) VALUES (?, ?, ?)", (username, filename, action))
    connection.commit()
    connection.close()

def get_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT filename, action, timestamp FROM history WHERE username = ? ORDER BY timestamp DESC",(username,))
    rows = cursor.fetchall()
    conn.close()
    return rows