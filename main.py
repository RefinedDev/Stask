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

        self.mainMenu = self.UIclass.create_Frame('springgreen2')

        versionLable = Label(self.mainMenu, text="V0.1",bg='springgreen2',font=('Arial',25))
        versionLable.pack(expand=True,fill='both',side='bottom')
        versionLable.place(relx = 0.98, rely = 1, anchor = 's')

        self.UIclass.create_Lable(parent=self.mainMenu,bg='springgreen2',isImage=True,textOrImage=self.menu_Image,width=400,height=250)

        viewListsButton = self.UIclass.create_Button(parent=self.mainMenu,bg='springgreen2',isImage=True,textOrImage=self.view_Image,width=200,height=50)
        # viewListsButton.config(command='eee')

        self.createPadding(self.mainMenu,1)
        
        createListsButton = self.UIclass.create_Button(parent=self.mainMenu,bg='springgreen2',isImage=True,textOrImage=self.create_Image,width=200,height=50)
        createListsButton.config(command = self.create_CreateListFrame)

        self.createPadding(self.mainMenu,1)

        deleteListsButton = self.UIclass.create_Button(parent=self.mainMenu,bg='springgreen2',isImage=True,textOrImage=self.delete_image,width=220,height=50)
        deleteListsButton.config(command=self.create_DeleteListFrame)

    def create_DeleteListFrame(self):
        """
        Create DeleteListFrame yes
        """
        self.mainMenu.destroy()
        playsound('Assets/clickSound.wav')

        self.deleteList = self.UIclass.create_Frame('springgreen2')
        databases = glob.glob("*DB")

        if len(databases) == 0:
            self.UIclass.create_Lable(parent=self.deleteList,bg='springgreen2',textOrImage='You have not created any Lists!',width=200,height=2)
            back = self.UIclass.create_Button(parent=self.deleteList,bg='red',textOrImage="Go Back",width=20,height=2,onClick='red3')
            back.config(command=self.create_MainMenu)
        else:
            self.currentSelection = self.UIclass.create_Lable(parent=self.deleteList,bg='springgreen2',textOrImage="Current Selection: None",width=50,height=2,isGrid=True,column=20,row=10)
            self.currentSelection.place(relx = 0.88, rely = 0.84, anchor = 's')

            currentColumn = 0
            currentRow = 0
            for i in databases:
                name = i.split(".DB")
                name = name[0]
                self.create_DeleteableObjects(self.deleteList,bg='goldenrod1',text=name,column=currentColumn,row=currentRow,width=30,height=2,onClick='goldenrod3')
                currentRow += 1
                if currentRow >= 5:
                    currentRow = 0
                    currentColumn += 1

            delete = self.UIclass.create_Button(parent=self.deleteList,bg='turquoise',textOrImage="Delete",width=20,height=2,onClick='dark turquoise',isGrid=True,column=20,row=10)
            delete.place(relx = 0.92, rely = 1, anchor = 's')
            delete.config(command=self.delete_List)

            back = self.UIclass.create_Button(parent=self.deleteList,bg='red',textOrImage="Back",width=20,height=2,onClick='red3',isGrid=True,column=20,row=10)
            back.place(relx = 0.92, rely = 0.92, anchor = 's')
            back.config(command=self.create_MainMenu)


    def create_CreateListFrame(self):
        """
        Create CreateListFrame yes.
        """
        self.mainMenu.destroy()
        playsound('Assets/clickSound.wav')

        self.createList = self.UIclass.create_Frame('springgreen2')

        self.UIclass.create_Lable(parent=self.createList,bg='springgreen2',textOrImage='Enter the list name.',width=200,height=2)

        inputLable = self.UIclass.create_InputLable(parent=self.createList,bg='springgreen2',width=50)
        self.createPadding(self.createList,1)

        create = self.UIclass.create_Button(parent=self.createList,bg='turquoise',textOrImage="Create List",width=20,height=2,onClick='dark turquoise')
        create.config(command=lambda : self.create_ListDatabase(inputLable))

        self.createPadding(self.createList,1)

        back = self.UIclass.create_Button(parent=self.createList,bg='red',textOrImage="Go Back",width=20,height=2,onClick='red3')
        back.config(command=self.create_MainMenu)

    def create_ListDatabase(self,inputLable):
        """
        Make the database for the list yes.
        """
        playsound('Assets/clickSound.wav')
        textWritten = inputLable.get()

        if hasattr(self,'resultLable'):
                self.resultLable.destroy()
                delattr(self,'resultLable')
            
        if len(textWritten) < 3:
            self.resultLable = self.UIclass.create_Lable(parent=self.createList,bg='springgreen2',textOrImage='Give the List a Longer Name (at least 3 letters)',width=200,height=2)
            return;
        elif not(os.path.exists(f'{textWritten}.DB')):
            self.resultLable = self.UIclass.create_Lable(parent=self.createList,bg='springgreen2',textOrImage='Creating list, please wait..',width=200,height=2)
        else:
            self.resultLable = self.UIclass.create_Lable(parent=self.createList,bg='springgreen2',textOrImage=f'List with the name "{textWritten}" already exists!',width=200,height=2)
            return;

        db = sqlite3.connect(f'{textWritten}.DB')
        cursor = db.cursor() 
        cursor.execute("CREATE TABLE IF NOT EXISTS pending(task TEXT NOT NULL, description TEXT NOT NULL, createdAt TEXT NOT NULL)")
        db.close()
        self.resultLable.config(text='To-Do List Created!')


    """
    HELPING FUNCTIONS
    """
    def create_DeleteableObjects(self,parent : str,bg : str,text : str,column : int,row : int,width : int,height : int,onClick : str):
        buttonObj = Button(parent,bg=bg,width=width,height=height,activebackground=onClick,relief=GROOVE,text=text,font=('Arial',10))
        buttonObj.grid(column=column,row=row)
        buttonObj.config(command=lambda : self.update_Selection_text(text))
        return buttonObj

    def createPadding(self,parent,height):
        self.UIclass.create_Lable(parent=parent,bg='springgreen2',textOrImage='',height=height)

    def update_Selection_text(self,name):
        self.currentSelection.config(text=f'{name}')

    def delete_List(self):
        text = self.currentSelection.cget("text")
        if text != 'Current Selection: None' and os.path.exists(f'{text}.DB'):
            os.remove(f'{text}.DB')
            self.deleteList.destroy()
            self.create_DeleteListFrame()

if __name__ == '__main__':
    app = Stask()
    app.create_MainMenu()
    app.UIobj.mainloop()