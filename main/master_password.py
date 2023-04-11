from Crypto.Protocol.KDF import PBKDF2
import hashlib
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

#in windows its called Crypto.Cipher and Crypto.Protocol.KDF
#in ubuntu it is called Cryptodome...

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#These are the functions to interact with the master password database, they are here for import reasons
import sqlite3

conn = sqlite3.connect("main.db")
c = conn.cursor()


def add_master_password(password, username):
    '''
    Inserts Master Password entry to mp database.
    '''
    with conn: 
        c.execute("INSERT INTO mp VALUES(:password, :username)", 
                                                    {'password': password, 
                                                        'username': username})

def get_master_password():
    '''
    Retrieves encrypted master password from mp database.
    '''
    c.execute("SELECT password FROM mp")
    return c.fetchone()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#These functions are the ones that interact with passwords and encryption                                                
salt = b'12\x1f\xdf\xfe\xf1R\xa3\x1ch\xd1\x15\xc2n;\xc2'



def verify_master_password(master_password):
    '''
    Checks if the master_password, when encrypted, is the same as the one in the mp database.
    '''
    master_password_hash = get_master_password()

    hashed_compilation = hashlib.sha256(master_password.encode()).hexdigest()
    hashed_compilation = (hashed_compilation,) 
    '''
    The above is due to the fact that when trying to do master_password_hash[0] 
    (since the hash is given back by the db in a tuple form) it gave an error because in an instance, 
    the function may return a None value, which cannot be accessed via [0]
    '''                   

    return hashed_compilation == master_password_hash



def encrypt_password(password_to_encrypt):
    '''
    Receives a password and encrypts it with the key obtained from the master password.
    '''

    master_password_hash = get_master_password()

    key = PBKDF2(str(master_password_hash), salt) 
                 
    #Converts password entered to byte string
    data_conversion = str.encode(password_to_encrypt)           

    cipher = AES.new(key, AES.MODE_EAX)                        
    nonce = cipher.nonce                                        
    ciphertext, MACtag = cipher.encrypt_and_digest(data_conversion)
    '''
    Adds the nonce to the already encrypted ciphertext, 
    this nonce will be then removed from the encrypted password and it will be used to create the 
    same cipher object in order to decrypt
    '''
    ciphertext_and_nonce = ciphertext + nonce              

    #This is what will be stored in the database
    encoded_ciphertext = b64encode(ciphertext_and_nonce).decode()

    return encoded_ciphertext                           


def decrypt_password(password_to_decrypt):
    master_password_hash = get_master_password()

    key = PBKDF2(str(master_password_hash), salt)
    
    password_bytes = b64decode(password_to_decrypt)            #Decodes the string into bytes

    nonce = password_bytes[-16:]                               #Takes from the 16th character to the end

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt(password_bytes[:-16])            #The first 16 characters

    return plaintext
    
    
