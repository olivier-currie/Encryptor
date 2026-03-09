# Encryptor

A full-stack Python desktop application for encrypting and decrypting files locally, with secure user authentication and a full activity history.

## Features

- **AES-256 encryption** — industry-standard symmetric encryption for protecting local files
- **Two-factor authentication** — account login verified via email-based 2FA
- **Encryption history** — full per-account log of all encryption and decryption activity
- **Local SQLite database** — lightweight, serverless storage for user accounts and history
- **Clean desktop UI** — built with a dedicated UI layer for a simple, user-friendly experience

## Tech Stack

- **Language:** Python
- **Encryption:** AES-256 (via `cryptography`)
- **Database:** SQLite
- **UI:** Tkinter

## Project Structure
```
Encryptor/
├── main.py        # Entry point
├── core/          # Encryption logic and authentication
├── db/            # Database models and queries
├── ui/            # Desktop interface components
└── assets/        # Icons and visual resources
```

## Getting Started
```bash
git clone https://github.com/olivier-currie/Encryptor.git
cd Encryptor
pip install -r requirements.txt
python main.py
```

## Credits

Icons by [Icons8](https://icons8.com)
