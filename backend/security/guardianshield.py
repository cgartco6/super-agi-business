from cryptography.fernet import Fernet
import hashlib
import os
from typing import Union

class GuardianShield:
    def __init__(self):
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        if not self.encryption_key:
            raise ValueError("Encryption key not configured")
        self.cipher_suite = Fernet(self.encryption_key)
    
    def encrypt_data(self, data: Union[str, dict]) -> str:
        """Encrypt sensitive data before storage"""
        if isinstance(data, dict):
            data = json.dumps(data)
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> Union[str, dict]:
        """Decrypt stored data when needed"""
        decrypted = self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        try:
            return json.loads(decrypted)
        except json.JSONDecodeError:
            return decrypted
    
    def verify_request(self, request: dict) -> bool:
        """Verify authenticity and integrity of incoming requests"""
        required_fields = {'timestamp', 'signature', 'client_id'}
        if not required_fields.issubset(request.keys()):
            return False
            
        # Verify request isn't too old
        if (datetime.now() - datetime.fromisoformat(request['timestamp'])).seconds > 300:
            return False
            
        # Verify signature
        expected_signature = self._generate_signature(
            request['client_id'],
            request['timestamp'],
            os.getenv('API_SECRET')
        )
        return request['signature'] == expected_signature
    
    def _generate_signature(self, client_id: str, timestamp: str, secret: str) -> str:
        """Generate HMAC signature for request verification"""
        message = f"{client_id}{timestamp}"
        return hashlib.sha256(
            (message + secret).encode()
        ).hexdigest()
