from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from base64 import b64encode
from base64 import b64decode


def encrypt(data, key):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(iv + data.encode())


def decrypt(data, key):
    iv = data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(data[AES.block_size:])


def cipher_as_str(cipher):
    return b64encode(cipher).decode()


def cipher_as_bytes(cipher):
    return b64decode(cipher).encode()


def password_digest(password):
    return SHA256.new(password.decode()).digest()
