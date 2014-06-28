from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from base64 import b64encode


def encrypt(plaintext, key):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(iv + plaintext)


def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(ciphertext[AES.block_size:]).decode()


def password_digest(password):
    password_bytes = b64encode(password.encode())
    return SHA256.new(password_bytes).digest()
