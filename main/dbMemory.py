from sqlite3 import connect

conn = connect("main.db")
c = conn.cursor()

def send_to_temp(website: str, username: str):
    '''
    Sends the website and username data to a temporary database to then retrieve them in the 
    next instance, the ShowPassword menu; in this menu the algorithm calls the db to ask for the password
    with the website and username provided from the temp db.
    '''
    with conn: 
        c.execute("INSERT INTO temp VALUES (:website, :username)", {'website': website, 'username':username})

def get_site():
    '''
    Gets entry data from the temp database to then ask the main database for the password.
    '''
    with conn:
        c.execute("SELECT * FROM temp")
        result = c.fetchone()        
        c.execute("DELETE FROM temp")
    return result
