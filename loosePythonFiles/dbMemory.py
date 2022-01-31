from sqlite3 import connect

conn = connect("main.db")
c = conn.cursor()

def send_to_temp(website, username):
    with conn: 
        c.execute("INSERT INTO temp VALUES (:website, :username)", {'website': website, 'username':username})

def get_site():
    with conn:
        c.execute("SELECT * FROM temp")
        result = c.fetchone()        
        c.execute("DELETE FROM temp")
    return result
