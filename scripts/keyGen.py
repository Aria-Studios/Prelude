from cryptography.fernet import Fernet

key = Fernet.generate_key()
key = key.decode('UTF-8')

print(key)
