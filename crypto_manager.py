import os
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

# In a real production environment, this key would be loaded from a secure environment variable or vault
# For this implementation, we will generate a stable key based on a system secret
SYSTEM_SECRET = os.getenv("SYSTEM_SECRET", "default-secret-key-change-this-in-prod")

class CryptoManager:
    def __init__(self):
        self.ph = PasswordHasher()
        self.encryption_key = self._derive_key(SYSTEM_SECRET)
        self.cipher = Fernet(self.encryption_key)

    def _derive_key(self, secret: str) -> bytes:
        """Derives a 32-byte key for AES encryption from the system secret."""
        salt = b'honeyword-salt-123' # Constant salt for deterministic key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(secret.encode()))

    # --- Password Hashing (Real Password) ---
    def hash_password(self, password: str) -> str:
        """Hashes a password using Argon2id."""
        return self.ph.hash(password)

    def verify_password(self, hashed: str, password: str) -> bool:
        """Verifies a password against an Argon2id hash."""
        try:
            return self.ph.verify(hashed, password)
        except Exception:
            return False

    # --- Honeyword Encryption (AES) ---
    def encrypt_honeyword(self, word: str) -> str:
        """Encrypts a honeyword using AES."""
        return self.cipher.encrypt(word.encode()).decode()

    def decrypt_honeyword(self, encrypted_word: str) -> str:
        """Decrypts a honeyword using AES."""
        return self.cipher.decrypt(encrypted_word.encode()).decode()

# Singleton instance for the application
crypto_manager = CryptoManager()
