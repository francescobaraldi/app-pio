from tkinter import *
import LoginPage
import ProfiloPage
from DBManager.DB import Database

class Home(Frame):
    def __init__(self, parent, controller, username):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.username = username
        self.db = Database()
        self.create_widgets()
    
    def create_widgets(self):
        self.login_label = Label(self, text=self.username, font=("bold", 25), pady=20)
        self.login_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.profilo_button = Button(self, text="Profilo", font=(18), width=10, command=lambda : self.controller.show_frame(ProfiloPage.Profilo, self.username))
        self.profilo_button.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.logout_button = Button(self, text="Logout", font=(18), width=10, command=lambda : self.controller.show_frame(LoginPage.Login))
        self.logout_button.place(relx=0.5, rely=0.7, anchor=CENTER)