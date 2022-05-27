from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    return key

def encrypt(data,key):
    return data
    # fernet = Fernet(key)
    # encrypted = fernet.encrypt(data)
    # return encrypted

def decrypt(data,key):
    return data
    # fernet = Fernet(key)
    # decrypted = fernet.decrypt(data)
    # decrypted = decrypted.decode()
    # return decrypted