import tkinter as tk
import sqlite3
from tkinter import messagebox
class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY , name TEXT, lastname TEXT, serial INTEGER, university TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS lectures (id INTEGER PRIMARY KEY , lectureName TEXT, semester INTEGER, serialTag INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS grades (id INTEGER PRIMARY KEY , lectureID TEXT, studentID, grade INTEGER )")

        self.conn.commit()

    def showStudents(self,student_list):
            
        student_list.delete(0, tk.END)
        for student in self.fetch():
            # print(student)    
            student_list.insert(tk.END, student)
        # print the entries in the console 

    def getStudentAsked(self,serialTag, student_list):
        self.cur.execute("SELECT * FROM students WHERE serial LIKE ? || '%'",(serialTag, ))
        student = self.cur.fetchall()
        student_list.delete(0, tk.END)
        for row in student:
            student_list.insert(tk.END,row)
        

    def fetch(self):
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()    
        # print (rows)
        return rows
        
    def check_if_exists(self,name,lastname):
        self.cur.execute("SELECT name FROM students WHERE name=? AND lastname=?", (name,lastname))
        rows = self.cur.fetchall()
        return rows

    def insert(self, lastname, firstname, serialtag,university):
        # self.checkEntrys(serialtag)
        
        self.cur.execute("SELECT COUNT (serial) FROM students WHERE serial = ? ",(serialtag,))
        rows = self.cur.fetchall()
        """
        rows variable returns a list containing a tuple
        if there is a student with the given serial tag show error message
        """
        if rows[0][0] != 0:
            messagebox.showerror('Λάθος Καταχώρηση','Υπάρχει ήδη φοιτητής με αυτόν τον αριθμό μητρώου ')
            return rows.count
        else:
            self.cur.execute("INSERT INTO students VALUES(NULL,?,?,?,?)", (lastname, firstname,serialtag, university))
            self.conn.commit()


    def remove(self,id):
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()

    def update(self,id , firstname,lastname, university, serialtag,student_list):
     

        self.cur.execute("UPDATE students SET lastname = ?, name = ?, university = ?, serial = ? WHERE id=?", (lastname, firstname, university,serialtag,id))
        self.conn.commit()
        self.showStudents(student_list)


    def fetchLectures(self):
        self.cur.execute("SELECT * FROM lectures")
        rows = self.cur.fetchall()
        
        return rows
    
    def check_if_lecture_exists(self,lectureID):
        self.cur.execute("SELECT * FROM lectures WHERE serialTag=?",(lectureID,))
        rows = self.cur.fetchall()
        # print(rows)
        return rows


    def addLecture(self, lecture, semester, serialNumber):

        res = self.check_if_lecture_exists(serialNumber)
        if len(res)>0:
            return messagebox.showerror('Error', 'Υπάρχει άλλο μάθημα με αυτό το αναγνωριστικό ID')
        else:
            self.cur.execute("INSERT INTO lectures VALUES(NULL,?,?,?)", (lecture,semester, serialNumber))
            self.conn.commit()
            self.fetchLectures()

    def delLectrueFromGrades(self,serial):
        self.cur.execute("DELETE FROM grades WHERE lectureId=?", (serial,))
        self.conn.commit()   

    def deleteLecture(self, id):
        self.delLectrueFromGrades(id)
        self.cur.execute("DELETE FROM lectures WHERE serialTag=?", (id,))
        self.conn.commit()


    def insertGrades(self, lectureID, studentSeriaTag, grade):
        self.cur.execute("INSERT INTO grades VALUES(NULL,?,?,?)", (lectureID, studentSeriaTag,grade))
        self.conn.commit()
    
    def fetchGrades(self,studentSeriaTag):
        self.cur.execute("SELECT lectureName,grade,lectureID FROM lectures,grades WHERE studentID=? AND grades.lectureID = lectures.serialTag",(studentSeriaTag,))
        rows = self.cur.fetchall()     
        # print (rows)
        return rows
    def deleteGrades(self):
        self.cur.execute("DELETE FROM grades")

    def checkForLecture(self,lectureID,serialTag):
        self.cur.execute("SELECT lectureID FROM grades WHERE lectureID=? AND studentID=?",(lectureID,serialTag))
        rows = self.cur.fetchall()
        return rows
   
    def mesosOros(self,studentID):
        self.cur.execute("SELECT AVG(grade) FROM grades WHERE studentID=? AND grade >= 5",(studentID,))
        row =self.cur.fetchone()
        row  = round(row[0],2)
        # print(row)
        return row
    
    def updateGrade(self,grade,lectureID,studentID):
        self.cur.execute("UPDATE grades SET grade=? WHERE lectureID =? AND studentID=? ",(grade,lectureID,studentID)) 
        self.conn.commit()

    def lecttureSum_Pass(self,studentID):
        self.cur.execute("SELECT COUNT(grade) FROM grades WHERE studentID=? ",(studentID,))
        allLectures = self.cur.fetchone()
        self.cur.execute("SELECT COUNT(grade) FROM grades WHERE studentID=? AND grade >= 5 ",(studentID,))
        passed = self.cur.fetchone()
       
        res = [allLectures,passed]
        return res

    def __del__(self):
        self.conn.close()


db = Database('students.db')

# db.insertGrades()
# res = db.mesosOros(6655)

# db.fetchGrades(4416031)



# db.addLecture('math', 2, 4556)