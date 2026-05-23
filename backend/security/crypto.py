import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from dotenv import load_dotenv

load_dotenv()

# Load AES secret key from environment variable
SECRET_KEY = os.getenv("AES_SECRET_KEY").encode()

def pad(data: bytes):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes):
    return data[:-data[-1]]

def aes_encrypt(plain_text: str):

    # Handle empty/null values safely
    if not plain_text:
        plain_text = ""

    iv = get_random_bytes(16)

    cipher = AES.new(
        SECRET_KEY,
        AES.MODE_CBC,
        iv
    )

    encrypted = cipher.encrypt(
        pad(plain_text.encode())
    )

    return (
        base64.b64encode(encrypted).decode(),
        base64.b64encode(iv).decode()
    )

def aes_decrypt(cipher_text: str, iv: str):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, base64.b64decode(iv))
    decrypted = cipher.decrypt(base64.b64decode(cipher_text))
    return unpad(decrypted).decode()

def compute_hash(data: str):
    return hashlib.sha256(data.encode()).hexdigest()