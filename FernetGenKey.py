from cryptography.fernet import Fernet

# Генерация нового ключа (выполнить один раз)
new_key = Fernet.generate_key()
print("NEW_FERNET_KEY:", new_key.decode())
