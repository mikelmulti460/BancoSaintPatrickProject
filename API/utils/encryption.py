import base64
from base64 import b64encode
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encrypter():
    def __init__(self,password,salt=os.urandom(16)):
        self.password = str(password).encode("utf-8")
        if type(salt)==str:
            self.salt = salt.encode("latin-1")
        if type(salt)==bytes:
            self.salt = salt
        self.token="" 
    
    def salt_text(self):
        salt = self.salt.decode("latin-1")
        return(salt)

    def generate_key(self):
        salt = self.salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key

    def encrypt_data(self,data):
        key = self.generate_key()
        f = Fernet(key)
        self.token = token = f.encrypt(f"{str(data)}".encode("utf-8"))
        return token.decode('utf-8')

    def decrypt_data(self,token):
        if type(token) == str:
            token.encode('utf-8')
        key = self.generate_key()
        f = Fernet(key)
        return {'data':f.decrypt(token).decode('utf-8'),'status':True }
