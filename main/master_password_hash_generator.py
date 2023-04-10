import hashlib

def master_password_hash_generator(master_password):
    return hashlib.sha256(master_password.encode()).hexdigest()

