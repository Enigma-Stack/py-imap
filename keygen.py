import os

def random_hex_string(length=32):
    return os.urandom(length).hex()

print(random_hex_string())