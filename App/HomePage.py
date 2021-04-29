from tkinter import *
from DBManager.DB import Database

class Home(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.db = Database()
        self.create_widgets()
    
    def create_widgets(self):
        self.login_label = Label(self, text="Questa è la homepage", font=("bold", 25), pady=20)
        self.login_label.place(relx=0.5, rely=0.1, anchor=CENTER)