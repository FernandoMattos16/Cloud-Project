import secrets

def generate_secret_key():
    return secrets.token_hex(32)

# Gera e exibe uma secret key
secret_key = generate_secret_key()
print("Secret Key:", secret_key)