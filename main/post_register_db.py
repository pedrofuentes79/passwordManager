import sqlite3

conn = sqlite3.connect("main.db")
c = conn.cursor()

def create_databases():
    '''
    Creates databases after the user registers
    '''
    with conn:
        c.execute("CREATE TABLE mp (password varchar(255), username varchar(255))") 
        c.execute("CREATE TABLE main (password varchar(255), website varchar(255), username varchar(255))")
        c.execute("CREATE TABLE temp (website varchar(255), username varchar(255))")
