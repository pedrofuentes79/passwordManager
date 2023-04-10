import sqlite3

conn = sqlite3.connect("main.db")
c = conn.cursor()

def get_encrypted_password(website: str, username: str):
    with conn:
        c.execute("SELECT * FROM main WHERE website=:website AND username=:username", 
                                        {'website': website, 'username': username})
    return c.fetchone()

def get_all_passwords():
    with conn:
        c.execute("SELECT * FROM main")
    return c.fetchall()

def add_password(encrypted_password: str, website: str, username: str):
        with conn: 
            c.execute("INSERT INTO main VALUES(:password, :website, :username)", 
                                                       {'password': encrypted_password, 
                                                        'website': website, 
                                                        'username': username})
                                                          
    
def edit_password(new_password: str, website: str):
    with conn:
        c.execute("UPDATE main SET password=:new_password WHERE website=:website", {'new_password': new_password, 'website': website})
    

def edit_username(new_username: str, website: str):
    with conn:
        c.execute("UPDATE main SET username=:new_username WHERE website=:website", {'new_username': new_username, 'website': website})

def delete_entry(website: str, username: str):
    with conn:
        c.execute("DELETE from main WHERE website=:website AND username=:username", {"website": website, "username": username})

def check_existing_entry(website: str, username: str):
    """Returns True if there is an existing entry, false otherwise"""
    with conn:
        c.execute("SELECT * FROM main WHERE website=:website AND username=:username", 
                                            {'website': website, 'username': username})    
        if c.fetchall() != []:
            return True
        else: 
            return False