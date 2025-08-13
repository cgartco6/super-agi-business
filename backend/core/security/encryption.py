from cryptography.fernet import Fernet
import base64
import os
from ..logging_setup import Logger
from ..config_manager import ConfigManager

class DataEncryptor:
    def __init__(self):
        self.config = ConfigManager()
        self.logger = Logger.get_logger(__name__)
        self.cipher_suite = self._initialize_cipher()

    def _initialize_cipher(self) -> Fernet:
        """Initialize encryption system"""
        key = self.config.get('security.encryption_key')
        if not key:
            self.logger.error("Encryption key not configured")
            raise ValueError("Encryption key missing")
        return Fernet(key.encode())

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        if isinstance(data, dict):
            import json
            data = json.dumps(data)
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            decrypted = self.cipher_suite.decrypt(encrypted_data.encode()).decode()
            try:
                import json
                return json.loads(decrypted)
            except ValueError:
                return decrypted
        except Exception as e:
            self.logger.error(f"Decryption failed: {str(e)}")
            raise

    def generate_key(self) -> str:
        """Generate new encryption key"""
        return Fernet.generate_key().decode()
