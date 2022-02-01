import hashlib

def master_password_hash_generator(master_password):
    hashed_master_password = hashlib.sha256(master_password.encode()).hexdigest()

    return hashed_master_password

