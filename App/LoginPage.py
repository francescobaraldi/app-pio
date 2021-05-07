from tkinter import *
import RegistrazionePage
import HomePage
from DBManager.DB import Database

class Login(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.db = Database()
        self.create_widgets()
    
    def create_widgets(self):
        self.login_label = Label(self, text="Effettua il login", font=("bold", 25), pady=20)
        self.login_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.username_label = Label(self, text="Username:", font=(18))
        self.username_label.place(relx=0.3, rely=0.2, anchor=CENTER)
        self.username_text = StringVar()
        self.username_textbox = Entry(self, width=30, textvariable=self.username_text)
        self.username_textbox.place(relx=0.5, rely=0.2, anchor=CENTER)
        
        self.password_label = Label(self, text="Password:", font=(18))
        self.password_label.place(relx=0.3, rely=0.3, anchor=CENTER)
        self.password_text = StringVar()
        self.password_textbox = Entry(self, width=30, textvariable=self.password_text, show="*")
        self.password_textbox.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.login_button = Button(self, text="Login", font=(18), width=10, command=self.login)
        self.login_button.place(relx=0.5, rely=0.4, anchor=CENTER)
        
        self.registrazione_button = Button(self, text="Non hai un account? Registrati", font=(18), command=lambda : self.controller.show_frame(RegistrazionePage.Registrazione))
        self.registrazione_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def login(self):
        users = self.db.read_user("*", "username", self.username_text.get())
        if(len(users) == 0):
            error = Label(self, text="Non esiste un utente con questo username.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.35, anchor=CENTER)
            return
        elif(users[0][3] != self.password_text.get()):
            error = Label(self, text="Password errata.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.35, anchor=CENTER)
            return
        self.controller.show_frame(HomePage.Home, self.username_text.get())