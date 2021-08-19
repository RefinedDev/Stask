from UIhandler import *
from playsound import playsound
import sqlite3
import glob
import os
import json

class Stask:
    def __init__(self):
        self.UIclass = StaskUIClass()
      
        self.menu_Image = PhotoImage(file= r"Assets\StaskLogo_NOBG.png")
        self.view_Image = PhotoImage(file= r"Assets\View_Lists.png")
        self.create_Image = PhotoImage(file= r"Assets\Create_List.png")
        self.delete_image = PhotoImage(file= r"Assets\Delete_List.png")

        self.UIobj = self.UIclass.UI
        self.UIobj.state('zoomed')    
 
        with open('settings.json') as f:
            data = json.load(f)
            
        self.BGColor = data['BackgroundColor']
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
            
        self.mainMenu = self.UIclass.create_Frame(self.BGColor)

        versionLable = Label(self.mainMenu, text="V0.1",bg=self.BGColor,font=('Arial',25))
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
        self.mainMenu.destroy()
        playsound('Assets/clickSound.wav')

        self.view_Lists_Frame = self.UIclass.create_Frame(self.BGColor)
        databases = glob.glob("*DB")

        if len(databases) == 0:
            self.UIclass.create_Lable(parent=self.view_Lists_Frame,bg=self.BGColor,textOrImage='You have not created any Lists!',width=200,height=2)
            back = self.UIclass.create_Button(parent=self.view_Lists_Frame,bg='red',textOrImage="Go Back",width=20,height=2,onClick='red3')
            back.config(command=self.create_MainMenu)
        else:
            self.currentColumn = 0
            self.currentRow = 0
            for i in databases:
                Grid.rowconfigure(self.view_Lists_Frame, self.currentRow, weight=1)
                Grid.columnconfigure(self.view_Lists_Frame, self.currentColumn, weight=1)

                name = i.split(".DB")
                name = name[0]
                self.create_viewListButton(self.view_Lists_Frame,bg='goldenrod1',text=name,column=self.currentColumn,row=self.currentRow,width=30,height=3,onClick='goldenrod3')
                self.currentRow += 1
                if self.currentRow >= 10:
                    self.currentRow = 0
                    self.currentColumn += 1
            
            back = self.UIclass.create_Button(parent=self.view_Lists_Frame,bg='red',textOrImage="Back",width=20,height=2,onClick='red3',isGrid=True,column=self.currentColumn,row=self.currentRow)
            back.config(command=self.create_MainMenu)

            Grid.rowconfigure(self.view_Lists_Frame, self.currentRow, weight=1)
            Grid.columnconfigure(self.view_Lists_Frame, self.currentColumn, weight=1)

    def view_TheList(self,name):
        for i in self.view_Lists_Frame.winfo_children():
            i.destroy()

        for i in range(self.currentColumn):
            Grid.columnconfigure(self.view_Lists_Frame, i, weight=0)
        
        for i in range(self.currentRow):
            Grid.rowconfigure(self.view_Lists_Frame, i, weight=0)

        delattr(self,'currentColumn')
        delattr(self,'currentRow')

        self.UIclass.create_Lable(parent=self.view_Lists_Frame,bg=self.BGColor,textOrImage='Pending',isGrid=True,column=0)
        self.UIclass.create_Lable(parent=self.view_Lists_Frame,bg=self.BGColor,textOrImage='Doing',isGrid=True,column=1).config(padx=500)
        self.UIclass.create_Lable(parent=self.view_Lists_Frame,bg=self.BGColor,textOrImage='Done',isGrid=True,column=2)

        createTask = self.UIclass.create_Button(parent=self.view_Lists_Frame,bg='turquoise',textOrImage="Create Task",width=10,height=1,onClick='dark turquoise',isGrid=True,column=2,row=2)
        createTask.config(command=lambda : self.create_Task(name))

        back = self.UIclass.create_Button(parent=self.view_Lists_Frame,bg='red',textOrImage="Back",width=10,height=1,onClick='red3',isGrid=True,column=3,row=2)
        back.config(command=self.create_MainMenu)

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
                Grid.columnconfigure(self.deleteList, currentColumn, weight=1)    
                name = i.split(".DB")
                name = name[0]
                self.create_DeletelistButton(self.deleteList,bg='goldenrod1',text=name,column=currentColumn,row=currentRow,width=30,height=3,onClick='goldenrod3')
                currentRow += 1
                if currentRow >= 10:
                    currentRow = 0
                    currentColumn += 1

            self.currentSelection = self.UIclass.create_Lable(parent=self.deleteList,bg=self.BGColor,textOrImage="None",isGrid=True,column=currentColumn + 1,row=currentRow)

            delete = self.UIclass.create_Button(parent=self.deleteList,bg='turquoise',textOrImage="Delete",width=20,height=2,onClick='dark turquoise',isGrid=True,column=currentColumn + 1,row=currentRow + 1)
            delete.config(command=self.delete_List)

            back = self.UIclass.create_Button(parent=self.deleteList,bg='red',textOrImage="Back",width=20,height=2,onClick='red3',isGrid=True,column=currentColumn + 1,row=currentRow + 2)
            back.config(command=self.create_MainMenu)
    
    def create_Task(self,text):
        self.view_Lists_Frame.destroy()
        delattr(self,'view_Lists_Frame')
        playsound('Assets/clickSound.wav')

        self.createTaskList = self.UIclass.create_Frame(self.BGColor)

        self.UIclass.create_Lable(parent=self.createTaskList,bg=self.BGColor,textOrImage='Enter the task name.',width=200,height=2)

        inputLable = self.UIclass.create_InputLable(parent=self.createTaskList,bg=self.BGColor,width=50)
        self.createPadding(self.createTaskList,1)

        create = self.UIclass.create_Button(parent=self.createTaskList,bg='turquoise',textOrImage="Create List",width=20,height=2,onClick='dark turquoise')
        create.config(command=lambda : self.create_task(text,inputLable))

        self.createPadding(self.createTaskList,1)

        back = self.UIclass.create_Button(parent=self.createTaskList,bg='red',textOrImage="Go Back",width=20,height=2,onClick='red3')
        back.config(command=self.create_MainMenu)

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
        if check  == 'exists':
            self.resultLable = self.UIclass.create_Lable(parent=self.createTaskList,bg=self.BGColor,textOrImage=f'List with the name "{textWritten}" already exists!',width=200,height=2)
            return;
        elif check == True:
            self.resultLable = self.UIclass.create_Lable(parent=self.createTaskList,bg=self.BGColor,textOrImage='Creating list, please wait..',width=200,height=2)
        else:
            self.resultLable = self.UIclass.create_Lable(parent=self.createTaskList,bg=self.BGColor,textOrImage='Give the List a Longer Name (at least 3 letters)',width=200,height=2)
            return;

        db = sqlite3.connect(f'{nameOfDB}.DB')
        cursor = db.cursor()
        
        cursor.execute(str.format("INSERT INTO pending (task) VALUES('%s')",textWritten))
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

    def create_viewListButton(self,parent : str,bg : str,text : str,column : int,row : int,width : int,height : int,onClick : str):
        buttonObj = Button(parent,bg=bg,width=width,height=height,activebackground=onClick,relief=GROOVE,text=text,font=('Arial',10,BOLD))
        buttonObj.grid(column=column,row=row)
        buttonObj.config(command=lambda : self.view_TheList(text))
        return buttonObj

    def createPadding(self,parent,height):
        self.UIclass.create_Lable(parent=parent,bg=self.BGColor,textOrImage='',height=height)

    def update_Selection_text(self,name):
        if hasattr(self,'currentSelection'):
            self.currentSelection.config(text=f'{name}')

    def delete_List(self):
        text = self.currentSelection.cget("text")
        if text != 'Current Selection: None' and os.path.exists(f'{text}.DB') and hasattr(self,'currentSelection'):
            os.remove(f'{text}.DB')
            self.deleteList.destroy()
            self.create_DeleteListFrame()

if __name__ == '__main__':
    app = Stask()
    app.create_MainMenu()
    app.UIobj.mainloop()