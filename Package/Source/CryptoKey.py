import pathlib

from cryptography.fernet import Fernet

def DecryptFernet(): 
    """
    Read secret key for Fernet cipher. 
    Call object Fernet. Decrypt encrypted text

    :return str:
    """
    with open(str(pathlib.Path(__file__).parents[1]) + '\\Resource\\FirstOfAll.key', 'rb') as File: 
        SecretKey = File.read()
    Cipher = Fernet(SecretKey)
    with open(str(pathlib.Path(__file__).parents[1]) + '\\Resource\\Something.key', 'rb') as f: 
        return str(Cipher.decrypt(f.read()).decode())