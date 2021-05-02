from tkinter import *
from tkinter import ttk
import HomePage
from DBManager.DB import Database

class Company(Frame):
    def __init__(self, parent, controller, username, name):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.username = username
        self.name = name
        self.db = Database()
        self.create_widgets()
    
    def create_widgets(self):
        self.login_label = Label(self, text=self.name, font=("bold", 19))
        self.login_label.place(relx=0.01, rely=0.01, anchor=NW)

        self.profilo_button = Button(self, text="Indietro", font=(18), width=10, command=lambda : self.controller.show_frame(HomePage.Home, self.username))
        self.profilo_button.place(relx=0.5, rely=0.9, anchor=NE)

