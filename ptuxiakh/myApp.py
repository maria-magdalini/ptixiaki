import tkinter as tk
from tkinter import ttk as table
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



db = Database('students.db')
    


class App(tk.Tk):
    
    def __init__(self):
               
        tk.Tk.__init__(self)
        #tk.Tk.iconbitmap = (self, default="icon.ico") change icon
        tk.Tk.wm_title(self, "University of Thessaly MS") # set title
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
   
    def studentSelect(self, event):
            global selected_item
            selected_item = self.student_list.get(ANCHOR)
            # PageTwo.labelChange()
      
            if len(selected_item) == 0:
                pass
            else:
                self.studentNameEntry.delete(0,tk.END)
                self.studentLastNameEntry.delete(0,tk.END)
                self.studentUniversityEntry.delete(0,tk.END)
                self.studentSerialTagEntry.delete(0,tk.END)

                
                    
                self.studentNameEntry.insert(tk.END,selected_item[1]),
                self.studentLastNameEntry.insert(tk.END,selected_item[2]),
                self.studentUniversityEntry.insert(tk.END,selected_item[4]),
                self.studentSerialTagEntry.insert(tk.END,selected_item[3])

            return selected_item

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        label = ttk.Label(self, text="Καταχώρηση Φοιτητή", font=LargeFont)
        label.pack(pady=10, padx=10)


      
        """       
          we need to pass the event in the studentSelect function because we bind it to the listbox 
          
        """     
        
                
        def clearInputs():
            self.studentNameEntry.delete(0,tk.END)
            self.studentLastNameEntry.delete(0,tk.END)
            self.studentUniversityEntry.delete(0,tk.END)
            self.studentSerialTagEntry.delete(0,tk.END)

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
        

        button = ttk.Button(self, text="Καταχώρη Βαθμών Και Μαθημάτων",
                            command=lambda: controller.show_frame(PageTwo) ) #acts as a onClick event
        button.pack(side='bottom',pady=10, padx=10)
        studentsFrame = tk.Frame(self)
        studentsFrame.pack(pady=5, padx=5 , fill='x')
        studentsFrame.config(bg="white")

        centerFrame = ttk.Frame(studentsFrame)
        
        centerFrame.pack()

        self.studentNameLabel = ttk.Label(centerFrame, text="Ονομα",background='white')
        self.studentNameLabel.pack( pady=10, padx=10, side="left")

        self.studentNameEntry = ttk.Entry(centerFrame, textvariable=studentName)
        self.studentNameEntry.pack( pady=10, padx=10, side="left") 

        self.studentLastNameLabel = ttk.Label(centerFrame, text="Επώνυμο",background='white')
        self.studentLastNameLabel.pack( pady=10, padx=10, side="left")

        self.studentLastNameEntry = ttk.Entry(centerFrame, textvariable=studentLastName)
        self.studentLastNameEntry.pack( pady=10, padx=10, side="left")

        self.studentSerialTagLabel = ttk.Label(centerFrame, text="Αριθμός Μητρώου",background='white')
        self.studentSerialTagLabel.pack( pady=10, padx=10, side="left")
        
        self.studentSerialTagEntry = ttk.Entry(centerFrame, textvariable=studentSerialTag)
        self.studentSerialTagEntry.pack( pady=10, padx=10, side="left")

        self.studentUniversityLabel = ttk.Label(centerFrame, text="Ονομα Σχολής",background='white')
        self.studentUniversityLabel.pack( pady=10, padx=10, side="left")
        
        self.studentUniversityEntry = ttk.Entry(centerFrame, textvariable=studentUniversity)
        self.studentUniversityEntry.pack( pady=10, padx=10, side="left")


        """
        Create a search bar for students
        """

        def search(e):
           entry = dataEntry.get()
           if entry =='':
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
        self.student_list.bind('<<ListboxSelect>>', self.studentSelect) 
        
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



class PageTwo(PageOne):
     
     
     def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        
        self.insertGradesLabel = ttk.Label(self, text="Καταχώρηση Βαθμών Φοιτητή", font=LargeFont)
        self.insertGradesLabel.pack(pady=10, padx=10)

        
 
        gradesFrame = tk.Frame(self)
        gradesFrame.pack()        
        
        
        lectureName = tk.Label(gradesFrame, text="Μάθημα")
        lectureName.pack(pady=10, padx=10,side='left')

        lectureValue = tk.StringVar()
        lectureEntry = tk.Entry(gradesFrame, text="none", textvariable=lectureValue)
        lectureEntry.pack(pady=10, padx=10,side='left')
        
        semester = tk.Label(gradesFrame, text="Εξάμηνο")
        semester.pack(pady=10, padx=10,side='left')

        semesterValue = tk.IntVar()
        semesterEntry = tk.Entry(gradesFrame, text="none",textvariable=semesterValue)
        semesterEntry.pack(pady=10, padx=10,side='left')

        lectureId = tk.Label(gradesFrame, text="ID Μαθήματος")
        lectureId.pack(pady=10, padx=10,side='left')

        lectureIdValue = tk.IntVar()
        lectureIdEntry = tk.Entry(gradesFrame, text="none",textvariable=lectureIdValue)
        lectureIdEntry.pack(pady=10, padx=10,side='left')

        """
        fetch lectures from db and display them in the tableview
        return all lectures in list contained each in its own tuple        
         like so [('Math', 1, 1233), ('Java', 1, 1244)]
        """
        a=db.fetchLectures() 
        lectures = []
        for i in a:
            i= list(i)
            i.pop(0)
            i = tuple(i)
            lectures.append(i)      
        
        
        columns = [
            {"text": "Μάθημα","stretch":False},
            {"text": "Εξάμηνο","stretch":False},
            {"text": "Κωδ. Μαθηματος","stretch":False}
            
        ]
        def showLecture():
            
            arr =[]
            for x in db.fetchLectures():
                x= list(x)
                x.pop(0)
                x=tuple(x)          
                arr.append(x)
                # print(x)
            return arr
        

         
        
        buttonsFrame = tk.Frame(self)
        buttonsFrame.pack(padx=10, pady=10)

        studentFrame = tk.LabelFrame(self, text='Καταχώρηση Βαθμών', font=('serif',14))
        studentFrame.pack(padx=10, pady=30)

        
        tablaFrame = tk.Frame(self)
        tablaFrame.pack(padx=10, pady=10)
        
        tree = Tableview(tablaFrame,autoalign=True, coldata=columns, rowdata=showLecture(),paginated=True,autofit=False,searchable=True)
        tree.pack(pady=10, padx=10,side='bottom')
        # row = tree.tablerows
       
        def clearEntrys():
            lectureEntry.delete(0, tk.END)
            semesterEntry.delete(0, tk.END)
            lectureIdEntry.delete(0, tk.END)
            showLecture()
        """
        get selected lecture and its values from Tableview
        see https://github.com/israel-dryer/ttkbootstrap/discussions/340
        """
        def selectItem(e):
            
            iid = tree.view.selection() # get the item selected from table 
            global selectionValue
            selectionValue = tree.view.item(iid,'values') # get the values from the selection in a tuple
            clearEntrys()
            lectureEntry.insert(tk.END, selectionValue[0])
            semesterEntry.insert(tk.END, selectionValue[1]) 
            lectureIdEntry.insert(tk.END, selectionValue[2]) 
            lectureToGradeEntry.delete(0,tk.END)
            lectureToGradeEntry.insert(tk.END, selectionValue[0])

        def delLecture(): # deletelecture
            iid = tree.view.selection()
            selectionValue 
            db.deleteLecture(selectionValue[2])
            tree.delete_rows(iids=iid) # delete the row from table after deleting lecture
            
        def tableReload():# reload the table function
            tree.delete_rows() #clear all rows in Tableview
            for x in db.fetchLectures(): #iterate through the tuples        
               x= list(x) #make each of them a list 
               x.pop(0) #remove the first item which is the row id from sqlite
               x= tuple(x)#make each list a tuple again because Tableview accepts tuples as rows
               
               
               tree.insert_row(tk.END, x)
            
           
            tree.load_table_data(clear_filters=True)

        def addL():#add lecture in db function
       
            db.addLecture(lectureValue.get(),semesterValue.get(),lectureIdValue.get())
            tableReload()
            
           
        
        tree.view.bind('<<TreeviewSelect>>', selectItem)
        # tree.build_table_data() # insert table
        # tree.load_table_data() #refresh table data

        
        

        chooseStudent = ttk.Button(buttonsFrame, text="Εισαγωγή Επιλεγμένου Φοιτητή", command=lambda : labelChange(self))      
        chooseStudent.pack(padx=10, pady=10, side='left')

        insertLecture = ttk.Button(buttonsFrame,text="Εισαγωγή μαθήματος",
                                   command= lambda : addL())
        insertLecture.pack(padx=10, pady=10, side='left')

        clearEntrysButton = ttk.Button(buttonsFrame,text="Απαλοιφή Πεδίων",bootstyle='danger',
                                   command= lambda : clearEntrys())
        clearEntrysButton.pack(padx=10, pady=10, side='left')

        deleteLecture = ttk.Button(buttonsFrame,text="Διαγραφή Μαθήματος",bootstyle='dark',
                                   command= lambda : delLecture())
        deleteLecture.pack(padx=10, pady=10, side='left')

        student= tk.Label(studentFrame, text="Όνομα Φοιτητή")
        student.pack(pady=10, padx=10,side='left')

        studentValue = tk.StringVar()
        studentEntry = tk.Entry(studentFrame, text="none", textvariable=studentValue, readonlybackground='YELLOW')
        studentEntry.pack(pady=10, padx=10,side='left')
        
       
        lectureToGrade = tk.Label(studentFrame, text="Μάθημα")
        lectureToGrade.pack(pady=10, padx=10,side='left')

        lectureToGradeValue = tk.StringVar()
        lectureToGradeEntry = tk.Entry(studentFrame, width=40,textvariable=lectureToGradeValue)
        lectureToGradeEntry.pack(pady=10, padx=10,side='left')

        grade = tk.Label(studentFrame, text="Βαθμός Μαθήματος")
        grade.pack(pady=10, padx=10,side='left')

        gradeValue = tk.IntVar()
        gradeEntry = tk.Entry(studentFrame, text="none",textvariable=gradeValue,width=2)
        gradeEntry.pack(pady=10, padx=10,side='left')

        insertGradesFrame = tk.Frame(studentFrame)
        insertGradesFrame.pack(pady=10, padx=10,side='bottom')

        insertGrade = ttk.Button(insertGradesFrame, text="Εισαγωγή Βαθμολογίας",bootstyle='success', command=lambda: checkStudentEntry())
        insertGrade.pack(pady=10, padx=10)

      

        def checkStudentEntry():
            entry = studentValue.get()
            if entry =='':
                messagebox.showerror("Μη Έγκυρη Εντολή",
                                     "Η Καταχώρηση Βαθμού δεν είναι δυνατή αν δεν επιλεγεί πρώτα καποιος φοιτητής.\nΕπιλέξτε πρώτα κάποιον φοιτητή και έπειτα πατήστε εισαγωγή ")

            else:
                name, lastname = entry.split()
                result = db.check_if_exists(name, lastname)
                if len(result) == 0 :
                    
                    messagebox.showerror('Error','Δεν υπάρχει αυτός ο φοιτητής')
                else:
                    db.insertGrades(lectureIdValue.get(),studentSeriaTag,gradeValue.get())
                    messagebox.showinfo('Success',"Ολοκληρώθηκε επιτυχώς ")
                print(len(result))

        #define top level window for user to see students grades
        def top():
            popup = Toplevel(self)
            homebutton = ttk.Button(popup, text="Back to home",
                            command=lambda: controller.show_frame(StartPage) ) #acts as a onClick event
            homebutton.pack(pady=10, padx=10)
            popup.mainloop()
               

        homebutton = ttk.Button(self, text="Back to home",
                            command=lambda: controller.show_frame(StartPage) ) #acts as a onClick event
        homebutton.pack(pady=10, padx=10)
        backToStudentsButton = ttk.Button(self, text="Go to page 1",
                            command=lambda: controller.show_frame(PageOne) ) #acts as a onClick event
        backToStudentsButton.pack(pady=10, padx=10)

        topLevelButton = ttk.Button(self, text="Εμφάνιση βαθμών φοιτητή",
                            command=lambda: top() ) #acts as a onClick event
        topLevelButton.pack(pady=10, padx=10)

        


        def labelChange(self):
            global studentSeriaTag 
             #am mathiti

            try:
                studentSeriaTag = selected_item[3]
                name = selected_item[1] +' '+selected_item[2] #onomateponumo
                print (studentSeriaTag)
                self.insertGradesLabel.config(text = name)
                
                if studentEntry.get() =='':
                    studentEntry.insert(0,name)
                else:
                    messagebox.showinfo('Reminder', 'Έχετε εισάγει ήδη έναν φοιτητή')
            
            except NameError :

                messagebox.showerror('Σφάλμα','Δεν έχει επιλεγεί κάποιος Φοιτητής. Η επιλογή φοιτητή ειναι υποχρεοτική για την εισαγωγή βαθμολογιών')
        



        
class PageThree(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graphs", font=LargeFont)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Back to home",
                            command=lambda: controller.show_frame(StartPage) ) #acts as a onClick event
        

        f= Figure(figsize=(10,4), dpi=100)
        a = f.add_subplot(111)  #1X1 CHART , CHART NO 1 -> (111)
        a.bar([1,2,3,4,5,6,7,8,9,1],'height') #X AXIS, Y AXIS FROM 0 TO 9 BOTH
        """
        students grades will be ploted when returned from the db 
        """
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