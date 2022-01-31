import sqlite3
from sqlite3.dbapi2 import OperationalError

conn = sqlite3.connect("main.db")
c = conn.cursor()

def get_password(website, username):
    with conn:
        c.execute("SELECT * FROM main WHERE website=:website AND username=:username", 
                                        {'website': website, 'username': username})
    return c.fetchone()


def add_password(password, website, username):
        with conn: 
            c.execute("INSERT INTO main VALUES(:password, :website, :username)", 
                                                       {'password': password, 
                                                        'website': website, 
                                                        'username': username})
                                                          
    
def edit_password(new_password, website):
    with conn:
        c.execute("UPDATE main SET password=:new_password WHERE website=:website", {'new_password': new_password, 'website': website})
    

def edit_username(new_username, website):
    with conn:
        c.execute("UPDATE main SET username=:new_username WHERE website=:website", {'new_username': new_username, 'website': website})

def delete_entry(website, username):
    with conn:
        c.execute("DELETE from main WHERE website=:website AND username=:username", {"website": website, "username": username})

def check_existing_entry(website, username):
    with conn:
        c.execute("SELECT * FROM main WHERE website=:website AND username=:username", 
                                            {'website': website, 'username': username})    
        if c.fetchall() != []:
            return True
        else: 
            return False