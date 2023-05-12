import sqlite3


class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY , name, lastname, university, serial)")
        self.conn.commit()


    def fetch(self):
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        return rows

    def insert(self, lastname, firstname, university,serialtag):
        self.cur.execute("INSERT INTO students VALUES(NULL,?,?,?,?)", (lastname, firstname, university,serialtag))
        self.conn.commit()


    def remove(self,id):
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()

    def update(self,id ,lastname, firstname, university, serialtag):
        self.cur.execute("UPDATE students SET lastname = ?, name = ?, university = ?, serial = ? WHERE id=?", (lastname, firstname, university,serialtag,id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

db = Database('students.db')

          
# db.insert('Ahmed','Ahmed','University','1234')  
