import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib as plt
plt.use('TkAgg')
import sqlite3
from db import Database 
db = Database


LargeFont  = ("serif", 12)

class App(tk.Tk):
    
    def __init__(self):
               
        tk.Tk.__init__(self)
        #tk.Tk.iconbitmap = (self, default="icon.ico") change icon
        tk.Tk.wm_title(self, "Managment System")
        container = tk.Frame(self)
        container.pack(side='top', fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames = {}
        for F in (StartPage, PageOne,PageTwo,PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
      
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()



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


    def fetchStudentsLecturesPassed(self,lecture,lectureGrade, studentName):
        self.cur.execute(f"SELECT * FROM lectures,students WHERE lectures.lectureGrade > 4 AND studentName='{studentName}' ",)

    def __del__(self):
        self.conn.close()

db = Database('students.db')
    
print(type(App))    


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame(parent, controller)
        
         
        

    def frame(self,parent, controller): 
       
               
        label = tk.Label(self, text="Start Page", font=LargeFont)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to page 1",
                            command=lambda: controller.show_frame(PageOne) ) #acts as a onClick event
        button.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="Go to page 2",
                            command=lambda: controller.show_frame(PageTwo) ) #acts as a onClick event
        button2.pack(pady=10, padx=10)
        button3 = ttk.Button(self, text="Go to Graphs",
                            command=lambda: controller.show_frame(PageThree) ) #acts as a onClick event
        button3.pack(pady=10, padx=10)





class PageOne(tk.Frame):
     
     
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame(controller)

     def frame(self, controller):   
        label = ttk.Label(self, text="Καταχώρηση Φοιτητή", font=LargeFont)
        label.pack(pady=10, padx=10)



        studentName = tk.StringVar()
        studentLastName = tk.StringVar()
        studentSerialTag = tk.StringVar()
        studentUniversity = tk.StringVar()
       

        button = ttk.Button(self, text="Go to page 2",
                            command=lambda: controller.show_frame(PageTwo) ) #acts as a onClick event
        button.pack(side='bottom',pady=10, padx=10)
        studentsFrame = tk.Frame(self)
        studentsFrame.pack(pady=5, padx=5 , fill='x')
        studentsFrame.config(bg="white")

        studentNameLabel = ttk.Label(studentsFrame, text="Ονομα",background='white')
        studentNameLabel.grid(row=0, column=0, pady=10, padx=10)

        studentNameEntry = ttk.Entry(studentsFrame, textvariable=studentName)
        studentNameEntry.grid(row=0, column=1,pady=10) 

        studentLastNameLabel = ttk.Label(studentsFrame, text="Επώνυμο",background='white')
        studentLastNameLabel.grid(row=1, column=0, pady=10, padx=10)

        studentLastNameEntry = ttk.Entry(studentsFrame, textvariable=studentLastName)
        studentLastNameEntry.grid(row=1, column=1, pady=10) 

        studentSerialTagLabel = ttk.Label(studentsFrame, text="Αριθμός Μητρώου",background='white')
        studentSerialTagLabel.grid(row=0, column=2, pady=10, padx=10)
        
        studentSerialTagEntry = ttk.Entry(studentsFrame, textvariable=studentSerialTag)
        studentSerialTagEntry.grid(row=0, column=3, pady=10) 

        studentUniversityLabel = ttk.Label(studentsFrame, text="Ονομα Σχολής",background='white')
        studentUniversityLabel.grid(row=1, column=2, pady=10, padx=10)
        
        studentUniversityEntry = ttk.Entry(studentsFrame, textvariable=studentUniversity)
        studentUniversityEntry.grid(row=1, column=3, pady=10) 

    
        student_list= tk.Listbox(self, height=10, width=70, border=0)
        student_list.pack(pady=10, padx=10)
        student_list.bind('<<ListboxSelect>>', self.fun) 

        showStudentButton = ttk.Button(self, text="Show students", command=lambda: self.fun(student_list))
        showStudentButton.pack(pady=10, padx=10)
        addStudentButton = ttk.Button(self, text="Add students", 
                                      command=lambda: self.insertStudent( studentName.get(), studentLastName.get(), 
                   studentUniversity.get(), studentSerialTag.get()))
        addStudentButton.pack(pady=10, padx=10)
     def values(self,studentName,studentLastName,studentUniversity,studentSerialTag):
         print(studentSerialTag)
         return [studentName,studentLastName,studentUniversity,studentSerialTag]
         
         

     def fun(self,student_list):
         student_list.delete(0, tk.END)
         for student in db.fetch():
             
             student_list.insert(tk.END,student)
            

     def insertStudent(self,studentName,studentLastName,studentUniversity,studentSerialTag):
         if studentName =='' or studentLastName=='' or studentUniversity=='' or studentSerialTag=='' :
            messagebox.showerror("Required Fields","Παρακαλώ συμπληρώστε όλα τα πεδία")
            return

         db.insert(studentName, studentLastName,studentUniversity,studentSerialTag)
         self.values(studentName,studentLastName,studentUniversity,studentSerialTag)
     
        

class PageTwo(tk.Frame):
  
     def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page two", font=LargeFont)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Back to home",
                            command=lambda: controller.show_frame(StartPage) ) #acts as a onClick event
        button.pack(pady=10, padx=10)
        button2 = ttk.Button(self, text="Go to page 1",
                            command=lambda: controller.show_frame(PageOne) ) #acts as a onClick event
        button2.pack(pady=10, padx=10)



class PageThree(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graphs", font=LargeFont)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Back to home",
                            command=lambda: controller.show_frame(StartPage) ) #acts as a onClick event
       

        f= Figure(figsize=(6,5), dpi=100)
        a = f.add_subplot(111)  #1X1 CHART , CHART NO 1 -> (111)
        a.plot([1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]) #X AXIS, Y AXIS FROM 0 TO 9 BOTH

        canvas = FigureCanvasTkAgg(f, master=self) #creating canvas
        canvas.draw() #drawing canvas
        canvas.get_tk_widget().pack(side=tk.TOP, fill='both', expand=True)#packing canvas to frame
        
        toobar = NavigationToolbar2Tk(canvas, self) # creating navigation
        toobar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill='both', expand=True) #packing mavigation toolbar to canvas
        button.pack(pady=10, padx=10)






app = App()
app.mainloop()
