import random
import string

def password_generator(length=20):
    '''
    Generates a random password of the given length
    '''
    characters = list(string.ascii_letters + string.digits + '!#$%&/()=?*{]}[')
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    
    random.shuffle(password)
    password = "".join(password)            #This takes every element from the list called password and joins them.
    return password

