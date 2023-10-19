import _sqlite3

conn = _sqlite3.connect("base.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (id integer UNIQUE, time integer)")

def add_id(id):
    c.execute("INSERT OR IGNORE INTO users (id, time) VALUES ('" + str(id) + "', '0')")
    conn.commit()

def change_time(id, time):
    c.execute("UPDATE users SET time = " + str(time) + " WHERE id = " + str(id))
    conn.commit()

def get(id):
    c.execute("SELECT time FROM users WHERE id = " + str(id))
    return c.fetchall()[0][0]