from tkinter import *
from tkinter import ttk
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
        self.login_label = Label(self, text="Benvenuto %s %s." % (self.db.read_user("nome", "username", self.username)[0][0], self.db.read_user("cognome", "username", self.username)[0][0]), font=("bold", 19))
        self.login_label.place(relx=0.01, rely=0.01, anchor=NW)

        self.profilo_button = Button(self, text="Profilo", font=(18), width=10, command=lambda : self.controller.show_frame(ProfiloPage.Profilo, self.username))
        self.profilo_button.place(relx=0.85, rely=0.01, anchor=NE)

        self.logout_button = Button(self, text="Logout", font=(18), width=10, command=lambda : self.controller.show_frame(LoginPage.Login))
        self.logout_button.place(relx=0.99, rely=0.01, anchor=NE)

        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.place(relx=0, rely=0.055, relwidth=2, relheight=0.02, anchor=N)

        self.interessi_frame = LabelFrame(self, text="I tuoi interessi", font=("bold", 18), height=20)
        self.interessi_frame.place(relx=0.2, rely=0.5, relheight=0.85, relwidth=0.3, anchor=CENTER)

        self.interessi_list = Listbox(self.interessi_frame)
        self.interessi_list.place(relx=0.47, rely=0.5, relheight=0.95, relwidth=0.85, anchor=CENTER)
        self.interessi_scrollbar = Scrollbar(self.interessi_frame)
        self.interessi_scrollbar.pack(side=RIGHT, fill=Y)
        self.interessi_list.configure(yscrollcommand=self.interessi_scrollbar.set)
        self.interessi_scrollbar.configure(command=self.interessi_list.yview)
        self.populate_interessi_list()

        self.consigliati_frame = LabelFrame(self, text="Esplora", font=("bold", 18), height=20)
        self.consigliati_frame.place(relx=0.5, rely=0.5, relheight=0.85, relwidth=0.3, anchor=CENTER)

        self.label = Label(self.consigliati_frame, text="Prova")
        self.label.pack()

        self.cerca_frame = LabelFrame(self, text="Cerca", font=("bold", 18), height=20)
        self.cerca_frame.place(relx=0.8, rely=0.5, relheight=0.85, relwidth=0.3, anchor=CENTER)

        self.label = Label(self.cerca_frame, text="Prova")
        self.label.pack()

    def populate_interessi_list(self):
        interessi = self.db.read_interested("name", "username", self.username)
        if(len(interessi) == 0):
            self.interessi_list.insert(END, "Non sei interessato a nessuna azienda")
            return
        for row in interessi:
            self.interessi_list.insert(END, row[0])