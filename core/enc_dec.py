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
    CHUNK_SIZE = 64 * 1024
    salt = os.urandom(16)
    key, iv = derive_key_iv(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    with open(filepath, 'rb') as fin, open(outpath, 'wb') as fout:
        fout.write(salt)

        while True:
            chunk = fin.read(CHUNK_SIZE)
            if not chunk:
                break
            if len(chunk) < CHUNK_SIZE:
                chunk = padder.update(chunk) + padder.finalize()
            else:
                chunk = padder.update(chunk)
            encrypted_chunk = encryptor.update(chunk)
            fout.write(encrypted_chunk)

        fout.write(encryptor.finalize())

def decrypt(filepath, outpath, password):
    CHUNK_SIZE = 64 * 1024
    with open(filepath, 'rb') as fin:
        salt = fin.read(16)
        key, iv = derive_key_iv(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()

        with open(outpath, 'wb') as fout:
            while True:
                chunk = fin.read(CHUNK_SIZE)
                if not chunk:
                    break
                decrypted_chunk = decryptor.update(chunk)
                if len(chunk) < CHUNK_SIZE:
                    decrypted_chunk = unpadder.update(decrypted_chunk) + unpadder.finalize()
                else:
                    decrypted_chunk = unpadder.update(decrypted_chunk)
                fout.write(decrypted_chunk)

            fout.write(decryptor.finalize())

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