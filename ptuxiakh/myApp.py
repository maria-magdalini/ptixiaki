import tkinter as tk
from tkinter import ttk as table
from tkinter import *
from tkinter import messagebox
from tkinter import ANCHOR # gets the selected item in the listbox
import ttkbootstrap as ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as mplt
import matplotlib as plt
plt.use('TkAgg')
import sqlite3
from db import Database 
import numpy as np
db = Database
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import matplotlib.ticker as ticker
from PIL import ImageTk, Image

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
        for F in (StartPage, PageOne,PageTwo):
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
        tk.Frame.__init__(self,parent,height=700,width=700)
       
    
        label = tk.Label(self, text="Διαχειριστικό Σύστημα Φοιτητών\nΠανεπιστήμιο Θεσσαλίας", font=LargeFont)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Διαχείριση Φοιτητών",
                            command=lambda: controller.show_frame(PageOne) ) #acts as a onClick event
        button.pack(pady=10, padx=10)

       

    
class PageOne(tk.Frame):
    
    def studentSelect(self, event):
            global selected_item
            selected_item = self.student_list.get(ANCHOR)
            # PageTwo.labelChange()
      
            if len(selected_item) == 0:
                pass
            else:
                # PageThree.main(PageThree,selected_item[3])
                self.studentNameEntry.delete(0,tk.END)
                self.studentLastNameEntry.delete(0,tk.END)
                self.studentUniversityEntry.delete(0,tk.END)
                self.studentSerialTagEntry.delete(0,tk.END)

                
                    
                self.studentNameEntry.insert(tk.END,selected_item[1]),
                self.studentLastNameEntry.insert(tk.END,selected_item[2]),
                self.studentUniversityEntry.insert(tk.END,selected_item[4]),
                self.studentSerialTagEntry.insert(tk.END,selected_item[3])
                
                print(selected_item[3])

            return selected_item

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        label = ttk.Label(self, text="Διαχείριση Φοιτητών", font=LargeFont)
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
            warning =  messagebox.askquestion('Οριστική Διαγραφη Φοιτητή', 'Θέλετε να διαγράψετε οριστικά αυτόν τον Φοιτητή ;')
            
            if warning =='no':
                pass
            else:
                
                print(warning)
                db.remove(selected_item[0])
                
                clearInputs()
                db.showStudents(self.student_list)

        
        studentName = tk.StringVar()
        studentLastName = tk.StringVar()
        global studentSerialTag
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
        
        self.scrollBar = ttk.Scrollbar(listFrame, bootstyle="secondary-round")
        self.scrollBar.pack(side='left',fill='y')
        
        
        self.student_list.configure(yscrollcommand=self.scrollBar.set)
        self.scrollBar.configure(command=self.student_list.yview)

        
        buttonsFrame = ttk.Frame(self)
        buttonsFrame.pack(padx=10, pady=10,)
       

        db.showStudents(self.student_list)
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
                    studentUniversity.get(), studentSerialTag.get(), self.student_list, selected_item[3]))
        updateButton.pack(pady=10, padx=10, side='left')
      

        
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
        
        
        self.insertGradesLabel = ttk.Label(self, text="Μαθήματα και Βαθμολογίες", font=LargeFont)
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
            warning =  messagebox.askquestion('Οριστική Διαγραφη Μαθήματος', 'Θέλετε να διαγράψετε οριστικά αυτό το Μάθημα ;')
            
            if warning =='no':
                pass
            else:
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
            
           
            tree.load_table_data()

        def addL():#add lecture in db function
            try:
                db.addLecture(lectureValue.get(),semesterValue.get(),lectureIdValue.get())
                tableReload()
            except:
                messagebox.showerror('Error','Το ID και το εξάμηνο πρέπει να είναι αριθμός')
           
            
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
        #the value of the student will be updated by clicking the chooseStudent button automatically
        studentEntry = tk.Entry(studentFrame, text="none", textvariable=studentValue,state='readonly')
        studentEntry.pack(pady=10, padx=10,side='left')
        
       
        lectureToGrade = tk.Label(studentFrame, text="Μάθημα")
        lectureToGrade.pack(pady=10, padx=10,side='left')

        lectureToGradeValue = tk.StringVar()
        lectureToGradeEntry = tk.Entry(studentFrame, width=40,textvariable=lectureToGradeValue)
        lectureToGradeEntry.pack(pady=10, padx=10,side='left')

        grade = tk.Label(studentFrame, text="Βαθμός Μαθήματος")
        grade.pack(pady=10, padx=10,side='left')

        gradeValue = DoubleVar()
        gradeEntry = tk.Entry(studentFrame, text="none",textvariable=gradeValue,width=5)
        gradeEntry.pack(pady=10, padx=10,side='left')

        insertGradesFrame = tk.Frame(studentFrame)
        insertGradesFrame.pack(pady=10, padx=10,side='bottom')

        insertGrade = ttk.Button(insertGradesFrame, text="Εισαγωγή Βαθμολογίας",bootstyle='success', command=lambda: checkStudentEntry())
        insertGrade.pack(pady=10, padx=10)

      

        def checkStudentEntry():
            try:
                hasBeenValued = checkForLecture(studentSeriaTag)
            except:
                messagebox.showerror("Μη Έγκυρη Εντολή",
                                     "Η Καταχώρηση Βαθμού δεν είναι δυνατή αν δεν επιλεγεί πρώτα καποιος φοιτητής.\nΕπιλέξτε πρώτα κάποιον φοιτητή και έπειτα πατήστε εισαγωγή ")
            print(hasBeenValued,)
            entry = studentValue.get()
            if entry == '':
                messagebox.showerror("Μη Έγκυρη Εντολή",
                                     "Η Καταχώρηση Βαθμού δεν είναι δυνατή αν δεν επιλεγεί πρώτα καποιος φοιτητής.\nΕπιλέξτε πρώτα κάποιον φοιτητή και έπειτα πατήστε εισαγωγή ")
            elif hasBeenValued>0:
                 messagebox.showerror('Error','Το μάθημα αυτό έχει ήδη βαθμολογηθεί')
            else:
                name, lastname = entry.split()
                result = db.check_if_exists(name, lastname)
                if len(result) == 0 :
                    
                    messagebox.showerror('Error','Δεν υπάρχει αυτός ο φοιτητής')
                else:
                    db.insertGrades(lectureIdValue.get(),studentSeriaTag,gradeValue.get())
                    messagebox.showinfo('Success',"Ολοκληρώθηκε επιτυχώς ")
                
        def checkForLecture(studentSeriaTag):
            res = db.checkForLecture(lectureIdValue.get(),studentSeriaTag)          
            return len(res)

        #define top level window for user to see students grades
        def top():
            val = studentValue.get()
            
            try:
                name, lastname = val.split()
                res = db.check_if_exists(name,lastname)
            except:
                messagebox.showerror('Error','Δεν έχει επιλεγεί κάποιος φοιτητής')
            print(res)
            
            if  val != '' and len(res)>0:
                popup = Toplevel(self)
                popup.wm_title(val +" AM: "+str(studentSeriaTag))
                columns = [
                
                {"text": "Μαθήμα","stretch":True},
                {"text": "Βαθμός","stretch":True},
                {"text": "ID Μαθήματος","stretch":True}
                
                ]

                rows = db.fetchGrades(studentSeriaTag)
                name = tk.Label(popup,text="Βαθμοί Μαθημάτων")
                name.pack()

                def selectLecute(e):
            
                    iid = studentsTree.view.selection() # get the item selected from table 
                    global lecture
                    lecture = studentsTree.view.item(iid,'values')
                    print(lecture[0]) # get the values from the selection in a tuple
                    # clearEntrys()
                    studentsLecture.configure(text=lecture[0]) 
                    studentsLectureEntry.delete(0,tk.END)   
                    studentsLectureEntry.insert(tk.END,lecture[1])

                studentsTree = Tableview(popup,autoalign=True, coldata=columns,rowdata=rows, paginated=True,autofit=False,searchable=True)
                studentsTree.pack(pady=10, padx=10)

                def updateMO(studentSeriaTag):
                    row = db.mesosOros(studentSeriaTag)
                    return row
                        
                studentsTree.view.bind('<<TreeviewSelect>>', selectLecute)
                buttonsFrame = tk.Frame(popup)
                buttonsFrame.pack(padx=10,pady=10)
                meter = ttk.Meter(
                    master=buttonsFrame,
                    metersize=180,
                    padding=5,
                    amounttotal=10,
                    amountused=updateMO(studentSeriaTag),
                    metertype="full",
                    subtext="M.O",
                    bootstyle='warning',
                    interactive=False,
                                         )
                meter.pack()

                lecturesSumFrame = tk.Frame(buttonsFrame)
                lecturesSumFrame.pack(padx=10,pady=20)

                lecturesSummary = tk.Label(lecturesSumFrame,text="Σύνολο Μαθημάτων: -\nΣύνολο Περασμενων Μαθημάτων: -" )
                lecturesSummary.pack(pady=20)

                def lectureUpdate(studentSeriaTag):
                    res = db.lecttureSum_Pass(studentSeriaTag)#returns a list of tuples
                    lecturesSummary.configure(text=f"Σύνολο Μαθημάτων: {res[0][0]}\nΣύνολο Περασμενων Μαθημάτων: {res[1][0]}")
                lectureUpdate(studentSeriaTag)
                updateGradesFrame = tk.Frame(buttonsFrame)
                updateGradesFrame.pack(padx=10,pady=10)
                studentsLecture = ttk.Label(updateGradesFrame, text=selectionValue[0] )
                studentsLecture.pack(pady=10, padx=10, side='left')

                studentsLectureValue = tk.DoubleVar()
                studentsLectureEntry= tk.Entry(updateGradesFrame, textvariable=studentsLectureValue)
                studentsLectureEntry.pack(pady=10, padx=10, side='left')
                
                

                homebutton = ttk.Button(updateGradesFrame, text="Αναβαθμολόγηση μαθήματος ",
                            command= lambda: reloadLectures(studentsLectureValue.get(),lecture[2],studentSeriaTag), bootstyle='outline-dark' ) #acts as a onClick event
                homebutton.pack(pady=10, padx=10, side='left')
                
                def graphs():
                    root = Toplevel()
                    root.wm_title(val +" AM: "+str(studentSeriaTag))
                    f= Figure(figsize=(10,4), dpi=100)        
                    a = f.add_subplot(111)  #1X1 CHART , CHART NO 1 -> (111)
                    #X AXIS, Y AXIS FROM 0 TO 9 BOTH
                
                
                    res=db.fetchGrades(studentSeriaTag)
                    print(res)
                    y = []

                    x = []

                    for i in res:

                        i = list(i)
                        i.pop(-1)
                        x.append(i[0])
                        y.append(i[1])
                    
                    a.bar(x,y,width=0.3, color='#ffbb33')
                    
                    a.set_ylim(0,10) # set the y range to 0-10
                    a.set_ylabel('Βαθμοί Μαθημάτων')
                    a.set_xlabel('Μαθήματα')
                    a.yaxis.set_major_locator(ticker.MultipleLocator(1)) #set the steps of ticker in y axis to 1
                    canvas = FigureCanvasTkAgg(f, master=root) #creating canvas
                    canvas.draw() #drawing canvas
                    canvas.get_tk_widget().pack(side=tk.TOP, fill='both', expand=True)#packing canvas to frame

                    toobar = NavigationToolbar2Tk(canvas,root) # creating navigation
                    toobar.update()
                    canvas._tkcanvas.pack(side=tk.TOP, fill='both', expand=True) #packing mavigation toolbar to canvas`

                    root.mainloop()
                homebutton = ttk.Button(updateGradesFrame, text="Γραφική Απεικόνιση Βαθμών ",bootstyle='outline-dark',
                            command=  graphs ) #acts as a onClick event
                homebutton.pack(pady=10, padx=10, side='left')
                def reloadLectures(lecture, lectureID, studentSeriaTag):
                    db.updateGrade(lecture,lectureID,studentSeriaTag)
                    db.mesosOros(studentSeriaTag)
                    
                    studentsTree.delete_rows()
                    for lecture in db.fetchGrades(studentSeriaTag):
                        studentsTree.insert_row(tk.END,lecture)
                    studentsTree.load_table_data()
                    meter.amountusedvar.set(db.mesosOros(studentSeriaTag))
                    lectureUpdate(studentSeriaTag)

                
                
               
                popup.mainloop()

            else:
                messagebox.showerror('Error','Δεν έχει επιλεγεί κάποιος φοιτητής')
               
        

       

        backToStudentsButton = ttk.Button(self, text="Διαχείρηση Φοιτητών",
                            command=lambda: chooseStudent() ) #acts as a onClick event
        backToStudentsButton.pack(pady=10, padx=10)

        topLevelButton = ttk.Button(self, text="Εμφάνιση βαθμών φοιτητή",
                            command=lambda: top(), bootstyle= "outline" ) #acts as a onClick event
        topLevelButton.pack(pady=10, padx=10)
        
        def chooseStudent():
            studentEntry.delete(0,tk.END)
            
            studentEntry.clipboard_clear()
            controller.show_frame(PageOne)
        


        def labelChange(self):
            global studentSeriaTag 
             #am mathiti

            try:
                studentSeriaTag = selected_item[3]
                name = selected_item[1] +' '+selected_item[2] #onomateponumo
                studentValue.set(name)
                # update the value of the student Entry based on the selection he made in the table 
                #prevents the user from typing nonsense
                print (studentSeriaTag)
                # self.insertGradesLabel.config(text = name)
                
                if studentEntry.get() =='' or studentEntry.get() != name:
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
        button.pack(pady=10, padx=10)
      
        """
        students grades will be ploted when returned from the db 
           if studentSerialTag==0:
            pass
        else:
            print(str(studentSerialTag)+'got student serial')
            f= Figure(figsize=(10,4), dpi=100)        
            a = f.add_subplot(111)  #1X1 CHART , CHART NO 1 -> (111)
            #X AXIS, Y AXIS FROM 0 TO 9 BOTH
        
           
            res=db.fetchGrades(studentSerialTag)
            print(res)
            y = []

            x = []

            for i in res:

                i = list(i)
                i.pop(-1)
                x.append(i[0])
                y.append(i[1])
            
            a.bar(x,y)
            canvas = FigureCanvasTkAgg(f, master=self) #creating canvas
            canvas.draw() #drawing canvas
            canvas.get_tk_widget().pack(side=tk.TOP, fill='both', expand=True)#packing canvas to frame

            toobar = NavigationToolbar2Tk(canvas, self) # creating navigation
            toobar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill='both', expand=True) #packing mavigation toolbar to canvas
        """
     
            
    def serialValue(value,self):
        print(value,self)
        self.main(self,value)
        
        
       
        



app = App()
# toast = ToastNotification(
#     title="Reminder",
#     message="This application was designed by Nikos Louzis",
#     duration=30000,
# )
# toast.show_toast()
app.mainloop()