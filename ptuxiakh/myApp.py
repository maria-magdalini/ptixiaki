import tkinter as tk
from tkinter import *
from tkinter import ANCHOR # gets the selected item in the listbox
import ttkbootstrap as ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib as plt
plt.use('TkAgg')
import sqlite3
from db import Database 
import numpy as np
db = Database
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview

LargeFont  = ("serif", 12)

class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY , name TEXT, lastname TEXT, serial INTEGER, university TEXT)")
        self.conn.commit()

    def showStudents(self,student_list):
            
        student_list.delete(0, tk.END)
        for student in self.fetch():
            
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
        for row in rows:
            for entry in row:
                print (row)
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


    def fetchStudentsLecturesPassed(self,lecture,lectureGrade, studentName):
        self.cur.execute(f"SELECT * FROM lectures,students WHERE lectures.lectureGrade > 4 AND studentName='{studentName}' ",)

    def __del__(self):
        self.conn.close()

db = Database('student.db')
    


class App(tk.Tk):
    
    def __init__(self):
               
        tk.Tk.__init__(self)
        #tk.Tk.iconbitmap = (self, default="icon.ico") change icon
        tk.Tk.wm_title(self, "Managment System") # set title
        container = tk.Frame(self) #Construct a frame widget with the parent MASTER.
        container.pack(side='top', fill="both", expand=True)
    
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames = {

        }
        for F in (StartPage, PageOne,PageTwo,PageThree):
            """
            we need to pass the self argument second because it is the App class
            witch it has showframe function and we give access to the ather pages
            through the controller argument.
            WE PACK OUT FRAMES INSIDE container wich belongs to the App class
            if we dont pass the self argument second we get the error that 
            Frame object has not an attribute show_frame, because now the controller
            is the tk.Frame itself which it has not access to show_frame() 
            
            """
            frame = F(container, self) #Construct a frame widget with the parent MASTER (self@App).
        
            self.frames[F] = frame #add the frame to the list of frames
            frame.grid(row=0,column=0, sticky='nesw ') #add the frame inside the window 
            # frame.pack()
        self.show_frame(StartPage)


    def show_frame(self,cont):
        frame = self.frames[cont]  #select the given frame  
        
        frame.tkraise() #then raise it to the top of stack 

  

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        #passing the parent in the StartPage like this (tk.Frame(App))
        #its like: frame(App) -> the frame is hosted in the Parent witch is App
        tk.Frame.__init__(self,parent)
        print(tk.Frame,type(parent))
        self.frame(controller)
       

    def frame(self,controller):         
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
         
        label = ttk.Label(self, text="Καταχώρηση Φοιτητή", font=LargeFont)
        label.pack(pady=10, padx=10)


        self.mainframe(controller,parent)
    
    def mainframe(self,controller,parent):
        """       
          we need to pass the event in the studentSelect function because we bind it to the listbox 
          
        """     
        def studentSelect(event):
            global selected_item
            selected_item = self.student_list.get(ANCHOR)
      
            if len(selected_item) == 0:
                pass
            else:
                studentNameEntry.delete(0,tk.END)
                studentLastNameEntry.delete(0,tk.END)
                studentUniversityEntry.delete(0,tk.END)
                studentSerialTagEntry.delete(0,tk.END)

                
                    
                studentNameEntry.insert(tk.END,selected_item[1]),
                studentLastNameEntry.insert(tk.END,selected_item[2]),
                studentUniversityEntry.insert(tk.END,selected_item[4]),
                studentSerialTagEntry.insert(tk.END,selected_item[3])

                
        def clearInputs():
            studentNameEntry.delete(0,tk.END)
            studentLastNameEntry.delete(0,tk.END)
            studentUniversityEntry.delete(0,tk.END)
            studentSerialTagEntry.delete(0,tk.END)

        def delete_student():
            warning =  messagebox.askquestion('Οριστική Διαγραφη Μαθητή', 'Θέλετε να διαγράψετε οριστικά αυτόν τον Μαθητή')

            if warning =='no':
                pass
            else:
                
                print(warning)
                db.remove(selected_item[0])
                
                clearInputs()
                db.showStudents(self.student_list)

        
        studentName = tk.StringVar()
        studentLastName = tk.StringVar()
        studentSerialTag = tk.IntVar()
        studentUniversity = tk.StringVar()
        

        button = ttk.Button(self, text="Go to page 2",
                            command=lambda: controller.show_frame(PageTwo) ) #acts as a onClick event
        button.pack(side='bottom',pady=10, padx=10)
        studentsFrame = tk.Frame(self)
        studentsFrame.pack(pady=5, padx=5 , fill='x')
        studentsFrame.config(bg="white")

        centerFrame = ttk.Frame(studentsFrame)
        
        centerFrame.pack()

        studentNameLabel = ttk.Label(centerFrame, text="Ονομα",background='white')
        studentNameLabel.pack( pady=10, padx=10, side="left")

        studentNameEntry = ttk.Entry(centerFrame, textvariable=studentName)
        studentNameEntry.pack( pady=10, padx=10, side="left") 

        studentLastNameLabel = ttk.Label(centerFrame, text="Επώνυμο",background='white')
        studentLastNameLabel.pack( pady=10, padx=10, side="left")

        studentLastNameEntry = ttk.Entry(centerFrame, textvariable=studentLastName)
        studentLastNameEntry.pack( pady=10, padx=10, side="left")

        studentSerialTagLabel = ttk.Label(centerFrame, text="Αριθμός Μητρώου",background='white')
        studentSerialTagLabel.pack( pady=10, padx=10, side="left")
        
        studentSerialTagEntry = ttk.Entry(centerFrame, textvariable=studentSerialTag)
        studentSerialTagEntry.pack( pady=10, padx=10, side="left")

        studentUniversityLabel = ttk.Label(centerFrame, text="Ονομα Σχολής",background='white')
        studentUniversityLabel.pack( pady=10, padx=10, side="left")
        
        studentUniversityEntry = ttk.Entry(centerFrame, textvariable=studentUniversity)
        studentUniversityEntry.pack( pady=10, padx=10, side="left")


        """
        Create a search bar for students
        """

        def search(e):
           entry = dataEntry.get()
           if entry ==' ':
               db.showStudents(self.student_list)
           else:
               db.getStudentAsked(entry, self.student_list)
          

        searchFrame = ttk.Frame(studentsFrame)
        searchFrame.pack( pady=10, padx=10, fill='x')

        searchLabel = ttk.Label(searchFrame, text="Αναζήτηση Φοιτητή (Βάση ΑΜ)",font=('serif',14))
        searchLabel.pack( pady=10, padx=10, )

        dataEntry = tk.IntVar()
        searchEntry = ttk.Entry(searchFrame, width=50,font=14, textvariable=dataEntry)
        searchEntry.pack()

        searchEntry.bind('<KeyRelease>', search)
        
         
       
                



    #create the list box wich the students are been displayed
        listFrame = ttk.Frame(self)
        listFrame.pack()

        self.student_list= tk.Listbox(listFrame, height=20, width=70, border=0)
        self.student_list.pack(pady=10, padx=10,side='left')
        #we need to pass the event in the studentSelect function because we bind it to the listbox 
        self.student_list.bind('<<ListboxSelect>>', studentSelect) 
        
        self.scrollBar = Scrollbar(listFrame, width=10)
        self.scrollBar.pack(side='left',fill='y')
        
        
        self.student_list.configure(yscrollcommand=self.scrollBar.set)
        self.scrollBar.configure(command=self.student_list.yview)


        buttonsFrame = ttk.Frame(self)
        buttonsFrame.pack(padx=10, pady=10,)
       


        showStudentButton = ttk.Button(buttonsFrame, text="Εμφάνιση Φοιτητών", command=lambda: db.showStudents(self.student_list))
        showStudentButton.pack(pady=10, padx=10,side='left')
    #button to add a new user in the database  
        addStudentButton = ttk.Button(buttonsFrame, text="Καταχώρηση Φοιτητή", 
                                        command=lambda: self.insertStudent(studentName.get(), studentLastName.get(), 
                    studentUniversity.get(), studentSerialTag.get() ))
        addStudentButton.pack(pady=10, padx=10, side='left')

        indexStudentButton = ttk.Button(buttonsFrame,bootstyle="danger", text="Διαγραφή Φοιτητή", command=delete_student)
        indexStudentButton.pack(pady=10, padx=10, side='left')
        
   
        updateButton=  ttk.Button ( buttonsFrame, text="Ανανέωση Στοιχείων", command= lambda : db.update(selected_item[0],studentName.get(), studentLastName.get(), 
                    studentUniversity.get(), studentSerialTag.get(), self.student_list))
        updateButton.pack(pady=10, padx=10, side='left')
      

        semesterA =  IntVar()
        semesterB =  IntVar()
        
     
       
        

    def insertStudent(self,studentName,studentLastName,studentUniversity,studentSerialTag):
        
        if studentName =='' or studentLastName=='' or studentUniversity=='' or studentSerialTag=='' :
            messagebox.showerror("Required Fields","Παρακαλώ συμπληρώστε όλα τα πεδία")
            return

        list =[studentName, studentLastName,studentUniversity]  
        for entry in (list):
        
            if entry[-1] == ' ' or entry[0] == ' ':
                messagebox.showerror("Εσφαλμένη Είσοδος",f"Δεν επιτέπετε η εισαγωγή κενών χαρακτήρων στην αρχή ή στο στο τέλος της εισόδου. Λάθος είσοδος : {entry}")
                return 
        
        db.insert(studentName,studentLastName,studentSerialTag,studentUniversity)
        db.showStudents(self.student_list)



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
       

        f= Figure(figsize=(10,4), dpi=100)
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
# toast = ToastNotification(
#     title="Reminder",
#     message="This application was designed by Nikos Louzis",
#     duration=30000,
# )
# toast.show_toast()
app.mainloop()
