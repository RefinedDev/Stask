from UIhandler import *
from playsound import playsound
import sqlite3
import glob
import os

class Stask:
    def __init__(self):
        self.UIclass = StaskUIClass()
      
        self.menu_Image = PhotoImage(file= r"Assets\StaskLogo_NOBG.png")
        self.view_Image = PhotoImage(file= r"Assets\View_Lists.png")
        self.create_Image = PhotoImage(file= r"Assets\Create_List.png")
        self.delete_image = PhotoImage(file= r"Assets\Delete_List.png")

        self.UIobj = self.UIclass.UI
        self.UIobj.state('zoomed')    
  
        self.BGColor = 'springgreen2'
    """
    IMPORTANT FUNCTIONS !!!!!!
    """
    def create_MainMenu(self):
        """
        The one the best and only, Creates MainMenuFrame yes.
        """
        if hasattr(self,'createList'):
            self.createList.destroy()
            playsound('Assets/clickSound.wav')
            delattr(self,'createList')
        elif hasattr(self,'deleteList'):
            self.deleteList.destroy()
            playsound('Assets/clickSound.wav')
            delattr(self,'deleteList')
        elif hasattr(self,'view_Lists_Frame'):
            self.view_Lists_Frame.destroy()
            playsound('Assets/clickSound.wav')
            delattr(self,'view_Lists_Frame')
        elif hasattr(self,'createTaskList'):
            self.createTaskList.destroy()
            playsound('Assets/clickSound.wav')
            delattr(self,'createTaskList')
        elif hasattr(self,'delete_Task_Frame'):
            self.delete_Task_Frame.destroy()
            playsound('Assets/clickSound.wav')
            delattr(self,'delete_Task_Frame')
        elif hasattr(self,'the_List'):
            self.the_List.destroy()
            playsound('Assets/clickSound.wav')
            delattr(self,'the_List')
            
        self.mainMenu = self.UIclass.create_Frame(self.BGColor)

        versionLable = Label(self.mainMenu, text="V0.3",bg=self.BGColor,font=('Arial',25))
        versionLable.pack(side='bottom',anchor=SE)

        self.UIclass.create_Lable(parent=self.mainMenu,bg=self.BGColor,isImage=True,textOrImage=self.menu_Image,width=400,height=250)

        viewListsButton = self.UIclass.create_Button(parent=self.mainMenu,bg=self.BGColor,isImage=True,textOrImage=self.view_Image,width=200,height=50)
        viewListsButton.config(command=self.create_ViewlistsFrame)

        self.createPadding(self.mainMenu,1)
        
        createListsButton = self.UIclass.create_Button(parent=self.mainMenu,bg=self.BGColor,isImage=True,textOrImage=self.create_Image,width=200,height=50)
        createListsButton.config(command = self.create_CreateListFrame)

        self.createPadding(self.mainMenu,1)

        deleteListsButton = self.UIclass.create_Button(parent=self.mainMenu,bg=self.BGColor,isImage=True,textOrImage=self.delete_image,width=220,height=50)
        deleteListsButton.config(command=self.create_DeleteListFrame)

    def create_ViewlistsFrame(self):
        """
        Creates View_Lists Frame Yes.
        """
        if hasattr(self,'the_List'):
            self.the_List.destroy()
            delattr(self,'the_List')
        else:
            self.mainMenu.destroy()

        playsound('Assets/clickSound.wav')

        self.view_Lists_Frame = self.UIclass.create_Frame(self.BGColor)
        databases = glob.glob("*DB")

        if len(databases) == 0:
            self.UIclass.create_Lable(parent=self.view_Lists_Frame,bg=self.BGColor,textOrImage='You have not created any Lists!',width=200,height=2)
            back = self.UIclass.create_Button(parent=self.view_Lists_Frame,bg='red',textOrImage="Go Back",width=20,height=2,onClick='red3')
            back.config(command=self.create_MainMenu)
        else:
            currentColumn = 0
            currentRow = 0
            for i in databases:
                Grid.rowconfigure(self.view_Lists_Frame, currentRow, weight=1)

                name = i.split(".DB")
                name = name[0]
                self.create_viewListButton(self.view_Lists_Frame,bg='goldenrod1',text=name,column=currentColumn,row=currentRow,width=30,height=3,onClick='goldenrod3')
                currentRow += 1
                if currentRow >= 10:
                    currentRow = 0
                    currentColumn += 1
            
            Grid.columnconfigure(self.view_Lists_Frame, currentColumn, weight=1)
            back = self.UIclass.create_Button(parent=self.view_Lists_Frame,bg='red',textOrImage="Back",width=20,height=2,onClick='red3',isGrid=True,column=currentColumn,row=currentRow)
            back.config(command=self.create_MainMenu)


    def view_TheList(self,name):
        playsound('Assets/clickSound.wav')

        if hasattr(self,'view_Lists_Frame'):
            self.view_Lists_Frame.destroy()
            delattr(self,'view_Lists_Frame')
        elif hasattr(self,'delete_Task_Frame'):
            self.delete_Task_Frame.destroy()
            delattr(self,'delete_Task_Frame')
        elif hasattr(self,'createTaskList'):
            self.createTaskList.destroy()
            delattr(self,'createTaskList')
        elif hasattr(self,'the_List'):
            self.the_List.destroy()

        self.the_List = self.UIclass.create_Frame(self.BGColor)
        
        db = sqlite3.connect(f'{name}.DB')
        cursor = db.cursor()

        cursor.execute("SELECT * FROM pending")
        result = cursor.fetchall()
        cursor.execute("SELECT * FROM doing")
        result2 = cursor.fetchall()
        cursor.execute("SELECT * FROM done")
        result3 = cursor.fetchall()
        
        self.UIclass.create_Lable(parent=self.the_List,bg=self.BGColor,textOrImage='Pending',isGrid=True,column=0)
        self.UIclass.create_Lable(parent=self.the_List,bg=self.BGColor,textOrImage='Doing',isGrid=True,column=1)
        self.UIclass.create_Lable(parent=self.the_List,bg=self.BGColor,textOrImage='Done',isGrid=True,column=2)

        currentRow = 1
        Grid.columnconfigure(self.the_List, 1, weight=1)

        for i in result:
            text = i[0]
            Grid.rowconfigure(self.the_List, currentRow, weight=1)
            self.create_TaskButton(self.the_List,bg='goldenrod1',text=text,column=0,row=currentRow,width=20,height=2,onClick='goldenrod3',dataBase=name)
            currentRow += 1

        currentRow = 1

        for i in result2:
            text = i[0]
            Grid.rowconfigure(self.the_List, currentRow, weight=1)
            self.create_TaskButton(self.the_List,bg='goldenrod1',text=text,column=1,row=currentRow,width=20,height=2,onClick='goldenrod3',dataBase=name)
            currentRow += 1

        currentRow = 1

        for i in result3:
            text = i[0]
            Grid.rowconfigure(self.the_List, currentRow, weight=1)
            self.create_TaskButton(self.the_List,bg='goldenrod1',text=text,column=2,row=currentRow,width=20,height=2,onClick='goldenrod3',dataBase=name)
            currentRow += 1

        currentRow = 1

        createTask = self.UIclass.create_Button(parent=self.the_List,bg='turquoise',textOrImage="Create Task",width=15,height=1,onClick='dark turquoise',isGrid=True,column=3,row=currentRow+1)
        createTask.config(command=lambda : self.create_Task(name))

        deleteTask = self.UIclass.create_Button(parent=self.the_List,bg='turquoise',textOrImage="Delete Task",width=15,height=1,onClick='dark turquoise',isGrid=True,column=3,row=currentRow +2)
        deleteTask.config(command=lambda : self.create_DeleteTaskFrame(name))

        back = self.UIclass.create_Button(parent=self.the_List,bg='red',textOrImage="Back",width=15,height=1,onClick='red3',isGrid=True,column=3,row=currentRow + 3)
        back.config(command=self.create_ViewlistsFrame)

    def create_DeleteListFrame(self):
        """
        Create DeleteListFrame yes
        """
        self.mainMenu.destroy()
        playsound('Assets/clickSound.wav')

        self.deleteList = self.UIclass.create_Frame(self.BGColor)
        databases = glob.glob("*DB")

        if len(databases) == 0:
            self.UIclass.create_Lable(parent=self.deleteList,bg=self.BGColor,textOrImage='You have not created any Lists!',width=200,height=2)
            back = self.UIclass.create_Button(parent=self.deleteList,bg='red',textOrImage="Go Back",width=20,height=2,onClick='red3')
            back.config(command=self.create_MainMenu)
        else:
            currentColumn = 0
            currentRow = 0
            for i in databases:
                Grid.rowconfigure(self.deleteList, currentRow, weight=1)
                name = i.split(".DB")
                name = name[0]
                self.create_DeletelistButton(self.deleteList,bg='goldenrod1',text=name,column=currentColumn,row=currentRow,width=30,height=3,onClick='goldenrod3')
                currentRow += 1
                if currentRow >= 10:
                    currentRow = 0
                    currentColumn += 1

            Grid.columnconfigure(self.deleteList, currentColumn, weight=1)    
            self.currentSelection = self.UIclass.create_Lable(parent=self.deleteList,bg=self.BGColor,textOrImage="None",isGrid=True,column=currentColumn + 1,row=currentRow)

            delete = self.UIclass.create_Button(parent=self.deleteList,bg='turquoise',textOrImage="Delete",width=20,height=2,onClick='dark turquoise',isGrid=True,column=currentColumn + 1,row=currentRow + 1)
            delete.config(command=self.delete_List)

            back = self.UIclass.create_Button(parent=self.deleteList,bg='red',textOrImage="Back",width=20,height=2,onClick='red3',isGrid=True,column=currentColumn + 1,row=currentRow + 2)
            back.config(command=self.create_MainMenu)
    
    def create_DeleteTaskFrame(self,dbName):
        """
        Create DeleteTaskFrame Yes.
        """
        if hasattr(self,'the_List'):
            self.the_List.destroy()
            delattr(self,'the_List')
            playsound('Assets/clickSound.wav')

        self.delete_Task_Frame = self.UIclass.create_Frame(self.BGColor)

        currentColumn = 0
        currentRow = 0
        db =  sqlite3.connect(f'{dbName}.DB')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM pending")
        result1 = cursor.fetchall()
        cursor.execute("SELECT * FROM doing")
        result1.extend(cursor.fetchall())
        cursor.execute("SELECT * FROM done")
        result1.extend(cursor.fetchall())
        
        for i in result1:
            Grid.rowconfigure(self.delete_Task_Frame, currentRow, weight=1)
            name = i[0]
            self.create_DeleteTaskButton(self.delete_Task_Frame,bg='goldenrod1',text=name,column=currentColumn,row=currentRow,width=30,height=3,onClick='goldenrod3')
            currentRow += 1
            if currentRow >= 10:
                currentRow = 0
                currentColumn += 1

        Grid.columnconfigure(self.delete_Task_Frame, currentColumn, weight=1)    
        self.currentSelection = self.UIclass.create_Lable(parent=self.delete_Task_Frame,bg=self.BGColor,textOrImage="None",isGrid=True,column=currentColumn + 1,row=currentRow)

        delete = self.UIclass.create_Button(parent=self.delete_Task_Frame,bg='turquoise',textOrImage="Delete",width=20,height=2,onClick='dark turquoise',isGrid=True,column=currentColumn + 1,row=currentRow + 1)
        delete.config(command= lambda : self.delete_Task(dbName))

        back = self.UIclass.create_Button(parent=self.delete_Task_Frame,bg='red',textOrImage="Back",width=20,height=2,onClick='red3',isGrid=True,column=currentColumn + 1,row=currentRow + 2)
        back.config(command=lambda : self.view_TheList(dbName))

        db.close()
    def create_Task(self,text):
        self.the_List.destroy()
        delattr(self,'the_List')
        playsound('Assets/clickSound.wav')

        self.createTaskList = self.UIclass.create_Frame(self.BGColor)

        self.UIclass.create_Lable(parent=self.createTaskList,bg=self.BGColor,textOrImage='Enter the task name.',width=200,height=2)

        inputLable = self.UIclass.create_InputLable(parent=self.createTaskList,bg=self.BGColor,width=50)
        self.createPadding(self.createTaskList,1)

        create = self.UIclass.create_Button(parent=self.createTaskList,bg='turquoise',textOrImage="Create List",width=20,height=2,onClick='dark turquoise')
        create.config(command=lambda : self.create_task(text,inputLable))

        self.createPadding(self.createTaskList,1)

        back = self.UIclass.create_Button(parent=self.createTaskList,bg='red',textOrImage="Go Back",width=20,height=2,onClick='red3')
        back.config(command=lambda : self.view_TheList(text))

    def create_CreateListFrame(self):
        """
        Create CreateListFrame yes.
        """
        self.mainMenu.destroy()
        playsound('Assets/clickSound.wav')

        self.createList = self.UIclass.create_Frame(self.BGColor)

        self.UIclass.create_Lable(parent=self.createList,bg=self.BGColor,textOrImage='Enter the list name.',width=200,height=2)

        inputLable = self.UIclass.create_InputLable(parent=self.createList,bg=self.BGColor,width=50)
        self.createPadding(self.createList,1)

        create = self.UIclass.create_Button(parent=self.createList,bg='turquoise',textOrImage="Create List",width=20,height=2,onClick='dark turquoise')
        create.config(command=lambda : self.create_ListDatabase(inputLable))

        self.createPadding(self.createList,1)

        back = self.UIclass.create_Button(parent=self.createList,bg='red',textOrImage="Go Back",width=20,height=2,onClick='red3')
        back.config(command=self.create_MainMenu)

    """
    HELPING FUNCTIONS
    """
    def create_task(self,nameOfDB,inputLable):
        playsound('Assets/clickSound.wav')
        textWritten = inputLable.get()

        if hasattr(self,'resultLable'):
            self.resultLable.destroy()
            delattr(self,'resultLable')

        check = self.UIclass.check_TextLength(textWritten,3)
        if check == True:
            self.resultLable = self.UIclass.create_Lable(parent=self.createTaskList,bg=self.BGColor,textOrImage='Creating list, please wait..',width=200,height=2)
        else:
            self.resultLable = self.UIclass.create_Lable(parent=self.createTaskList,bg=self.BGColor,textOrImage='Give the List a Longer Name (at least 3 letters)',width=200,height=2)
            return;

        db = sqlite3.connect(f'{nameOfDB}.DB')
        cursor = db.cursor()
        
        cursor.execute(f"INSERT INTO pending (task) VALUES('{textWritten}')")
        db.commit()
        db.close()
        self.resultLable.config(text='Task Created!')
        
    def create_ListDatabase(self,inputLable):
        """
        Make the database for the list yes.
        """
        playsound('Assets/clickSound.wav')
        textWritten = inputLable.get()

        if hasattr(self,'resultLable'):
            self.resultLable.destroy()
            delattr(self,'resultLable')

        check = self.UIclass.check_TextLength(textWritten,3)
        if check  == 'exists':
            self.resultLable = self.UIclass.create_Lable(parent=self.createList,bg=self.BGColor,textOrImage=f'List with the name "{textWritten}" already exists!',width=200,height=2)
            return;
        elif check == True:
            self.resultLable = self.UIclass.create_Lable(parent=self.createList,bg=self.BGColor,textOrImage='Creating list, please wait..',width=200,height=2)
        else:
            self.resultLable = self.UIclass.create_Lable(parent=self.createList,bg=self.BGColor,textOrImage='Give the List a Longer Name (at least 3 letters)',width=200,height=2)
            return;

        db = sqlite3.connect(f'{textWritten}.DB')
        cursor = db.cursor() 
        cursor.execute("CREATE TABLE IF NOT EXISTS pending(task TEXT NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS doing(task TEXT NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS done(task TEXT NOT NULL)")
        db.close()
        self.resultLable.config(text='To-Do List Created!')

    def create_DeletelistButton(self,parent : str,bg : str,text : str,column : int,row : int,width : int,height : int,onClick : str):
        buttonObj = Button(parent,bg=bg,width=width,height=height,activebackground=onClick,relief=GROOVE,text=text,font=('Arial',10,BOLD))
        buttonObj.grid(column=column,row=row)
        buttonObj.config(command=lambda : self.update_Selection_text(text))
        return buttonObj

    def create_DeleteTaskButton(self,parent : str,bg : str,text : str,column : int,row : int,width : int,height : int,onClick : str):
        buttonObj = Button(parent,bg=bg,width=width,height=height,activebackground=onClick,relief=GROOVE,text=text,font=('Arial',10,BOLD))
        buttonObj.grid(column=column,row=row)
        buttonObj.config(command=lambda : self.update_Selection_text(text))
        return buttonObj

    def create_viewListButton(self,parent : str,bg : str,text : str,column : int,row : int,width : int,height : int,onClick : str):
        buttonObj = Button(parent,bg=bg,width=width,height=height,activebackground=onClick,relief=GROOVE,text=text,font=('Arial',10,BOLD))
        buttonObj.grid(column=column,row=row)
        buttonObj.config(command=lambda : self.view_TheList(text))
        return buttonObj

    def create_TaskButton(self,parent : str,bg : str,text : str,column : int,row : int,width : int,height : int,onClick : str,dataBase : str):
        buttonObj = Button(parent,bg=bg,width=width,height=height,activebackground=onClick,relief=GROOVE,text=text,font=('Arial',10,BOLD))
        buttonObj.grid(column=column,row=row)
        buttonObj.config(command=lambda : self.make_Button_Done_Pending_Doing(column,dataBase,text))
        return buttonObj

    def make_Button_Done_Pending_Doing(self,column,database,text):
        db = sqlite3.connect(f'{database}.DB')
        cursor = db.cursor()
        if column == 0: # Was Pending Now Doing
            cursor.execute(f"INSERT INTO doing (task) VALUES('{text}')")
            cursor.execute(f"DELETE FROM pending WHERE task = '{text}'")
            db.commit()
        elif column == 1: # Was Doing Now Done
            cursor.execute(f"INSERT INTO done (task) VALUES('{text}')")
            cursor.execute(f"DELETE FROM doing WHERE task = '{text}'")
            db.commit()
        elif column == 2: # Done Now Pending
            cursor.execute(f"INSERT INTO pending (task) VALUES('{text}')")
            cursor.execute(f"DELETE FROM done WHERE task = '{text}'")
            db.commit()
        self.view_TheList(database)
        db.close()
        
    def createPadding(self,parent,height):
        self.UIclass.create_Lable(parent=parent,bg=self.BGColor,textOrImage='',height=height)

    def update_Selection_text(self,name):
        playsound('Assets/clickSound.wav')
        
        if hasattr(self,'currentSelection'):
            self.currentSelection.config(text=f'{name}')

    def delete_List(self):
        text = self.currentSelection.cget("text")
        if text != 'Current Selection: None' and os.path.exists(f'{text}.DB') and hasattr(self,'currentSelection'):
            os.remove(f'{text}.DB')
            self.deleteList.destroy()
            self.create_DeleteListFrame()

    def delete_Task(self,dBNAME):
        text = self.currentSelection.cget("text")
        db = sqlite3.connect(f'{dBNAME}.DB')
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM pending WHERE task = '{text}'")
        if len(cursor.fetchall()) != 0:
            cursor.execute(f"DELETE FROM pending WHERE task = '{text}'")
        else:
            cursor.execute(f"SELECT * FROM doing WHERE task = '{text}'")
            if len(cursor.fetchall()) != 0:
                cursor.execute(f"DELETE FROM doing WHERE task = '{text}'")
            else:
                cursor.execute(f"SELECT * FROM done WHERE task = '{text}'")
                if len(cursor.fetchall()) != 0:
                    cursor.execute(f"DELETE FROM done WHERE task = '{text}'")

        db.commit()
        db.close()
        self.delete_Task_Frame.destroy()
        self.create_DeleteTaskFrame(dBNAME)

if __name__ == '__main__':
    app = Stask()
    app.create_MainMenu()
    app.UIobj.mainloop()