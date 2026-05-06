# Honeyword Intrusion Detection System (IDS)

## Overview
This project is an advanced Intrusion Detection System (IDS) built around the concept of **Honeywords**. Honeywords are decoy passwords associated with a user's account alongside their real password. If a database is ever compromised and passwords are stolen, an attacker attempting to use one of the decoy honeywords to log in will instantly trigger a silent alarm, alerting administrators to the breach while granting the attacker "fake" access so they don't realize they've been caught.

This system was developed as a Final Year Project to demonstrate advanced concepts in database security, cryptography, and intrusion detection.

## Key Features
- **Secure Password Hashing**: Real user passwords are hashed using state-of-the-art cryptographic algorithms (Argon2id) before being stored in the database.
- **Automated Honeyword Generation**: Upon registration, the system automatically generates multiple decoy passwords (honeywords) that closely resemble human-chosen passwords to fool attackers.
- **Honeyword Encryption**: Honeywords are stored securely using AES encryption to prevent trivial extraction.
- **Silent Intrusion Alerts**: When an attacker attempts to log in using a honeyword, the system triggers a background alert (via `alert_system.py`) logging the intrusion, the targeted username, and the honeyword used. The attacker is given a successful login response to avoid tipping them off.
- **FastAPI Backend**: The core logic is built on FastAPI, providing a fast, modern, and robust RESTful API.
- **PostgreSQL Integration**: Data is stored reliably in a PostgreSQL database.

## Technology Stack
- **Backend Framework**: Python (FastAPI)
- **Database**: PostgreSQL
- **Cryptography**: `cryptography` (AES for honeywords), Argon2id (for real passwords)
- **Database Driver**: `psycopg2`

## Project Structure
- `main.py`: The entry point for the FastAPI application containing the `/register` and `/login` routes.
- `crypto_manager.py`: Handles all cryptographic operations, including hashing real passwords and encrypting/decrypting honeywords.
- `honeyword_generator.py`: Contains the logic to generate convincing decoy passwords.
- `alert_system.py`: Manages the intrusion detection alerts and logs them (e.g., to `intrusion_alerts.log`).
- `schema.sql`: The SQL schema used to set up the PostgreSQL database tables (`users` and `honeywords`).
- `CHAPTERS/`: Contains the project documentation, research methodology, and final report drafts.
- `venv/`: The Python virtual environment for managing dependencies.

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd Final_year_project
   ```

2. **Set up the Virtual Environment:**
   Make sure you have Python installed, then activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. **Database Configuration:**
   Ensure PostgreSQL is running. Create a database (default name `honeyword_db`) and run the `schema.sql` to create the necessary tables. You can configure database credentials using environment variables:
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_HOST`
   - `DB_PORT`

4. **Run the Application:**
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

5. **API Endpoints:**
   - `POST /register`: Accepts `username` and `password`. Creates the user, hashes the password, and generates/encrypts honeywords.
   - `POST /login`: Accepts `username` and `password`. Checks the real password. If it fails, checks the honeywords. If a honeyword matches, it triggers an alert.

## Documentation
The complete project documentation, including the Introduction, Literature Review, and system design, can be found in the `CHAPTERS/` directory.