import os
from tkinter import *
from tkinter.font import BOLD

class StaskUIClass:
    def __init__(self):
        self.UI = Tk()
        self.UI.resizable(0,0)
        
        self.TOP_icon = PhotoImage(file= r"Assets\StaskLogo.png")

        self.UI.iconphoto(False, self.TOP_icon)
        self.UI.title('Stask')
        

    def create_Frame(self,bg):
        frame = Frame(self.UI,bg=bg)
        frame.pack(fill="both", expand=True)
        return frame

    def create_Lable(self,parent : str,bg : str,isImage : bool = False,textOrImage : PhotoImage = None,isGrid : bool = False,side='top',column : int = 0,row : int = 0,width : int = 0,height : int = 0):
        lableObj = Label(parent,bg=bg,width=width,height=height)
        if isImage:
            lableObj.config(image=textOrImage)
        else:
            lableObj.config(text=textOrImage,font=("Arial", 25,BOLD),fg='black')
        
        if not (isGrid):
            lableObj.pack(side=side)
        else:
            lableObj.grid(column=column,row=row)

        return lableObj

    def create_Button(self,parent : str,bg : str,isImage : bool = False,textOrImage : PhotoImage = None,isGrid : bool = False,side='top',column : int = 0,row : int = 0,width : int = 0,height : int = 0,padx = 0, pady = 0,onClick : str = 'springgreen3'):
        buttonObj = Button(parent,bg=bg,width=width,height=height,padx=padx,pady=pady,activebackground=onClick,relief=GROOVE)
        if isImage:
            buttonObj.config(image=textOrImage)
        else:
            buttonObj.config(text=textOrImage,font=("Arial", 15,BOLD),fg='black')

        if not (isGrid):
            buttonObj.pack(side=side)
        else:
            buttonObj.grid(column=column,row=row)
    
        return buttonObj
    
    def create_InputLable(self,parent : str,bg : str,isGrid : bool = False,side='top',column : int = 0,row : int = 0,width : int = 0):
        inputObj = Entry(parent,bg=bg,width=width,font=("Arial",25),borderwidth=5,relief=GROOVE)
        if not (isGrid):
            inputObj.pack(side=side)
        else:
            inputObj.grid(column=column,row=row)

        return inputObj
    
    def check_TextLength(self,text,limit):
        textWritten = text

        if len(textWritten) < limit:
            return False;
        elif not(os.path.exists(f'{textWritten}.DB')):
            return True;
        else:
            return 'exists';