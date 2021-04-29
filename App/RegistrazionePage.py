from tkinter import *
from tkinter import messagebox
from HomePage import Home
from DBManager.DB import Database

class Registrazione(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = Database()
        self.create_widgets()
    
    def create_widgets(self):
        self.register_label = Label(self, text="Registrazione", font=("bold", 25), pady=20)
        self.register_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.nome_label = Label(self, text="Nome:", font=(18))
        self.nome_label.place(relx=0.3, rely=0.2, anchor=CENTER)
        self.nome_text = StringVar()
        self.nome_textbox = Entry(self, width=20, textvariable=self.nome_text)
        self.nome_textbox.place(relx=0.5, rely=0.2, anchor=CENTER)
        
        self.cognome_label = Label(self, text="Cognome:", font=(18))
        self.cognome_label.place(relx=0.3, rely=0.3, anchor=CENTER)
        self.cognome_text = StringVar()
        self.cognome_textbox = Entry(self, width=20, textvariable=self.cognome_text)
        self.cognome_textbox.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.username_label = Label(self, text="Username:", font=(18))
        self.username_label.place(relx=0.3, rely=0.4, anchor=CENTER)
        self.username_text = StringVar()
        self.username_textbox = Entry(self, width=20, textvariable=self.username_text)
        self.username_textbox.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.password_label = Label(self, text="Password:", font=(18))
        self.password_label.place(relx=0.3, rely=0.5, anchor=CENTER)
        self.password_text = StringVar()
        self.password_textbox = Entry(self, width=20, textvariable=self.password_text, show="*")
        self.password_textbox.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.conferma_password_label = Label(self, text="Conferma password:", font=(18))
        self.conferma_password_label.place(relx=0.3, rely=0.6, anchor=CENTER)
        self.conferma_password_text = StringVar()
        self.conferma_password_textbox = Entry(self, width=20, textvariable=self.conferma_password_text, show="*")
        self.conferma_password_textbox.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.registrazione_button = Button(self, text="Registrati", font=(18), width=10, command=lambda : self.registrato())
        self.registrazione_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.indietro_button = Button(self, text="Indietro", font=(18), width=10, command=lambda : self.controller.show_frame(Home))
        self.indietro_button.place(relx=0.5, rely=0.8, anchor=CENTER)

    def registrato(self):
        if(len(self.nome_text.get()) < 3):
            error = Label(self, text="Errore: nome troppo corto.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.65, anchor=CENTER)
            return
        if(len(self.cognome_text.get()) < 2):
            error = Label(self, text="Errore: cognome troppo corto.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.65, anchor=CENTER)
            return
        if(len(self.username_text.get()) < 3):
            error = Label(self, text="Errore: username troppo corto.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.65, anchor=CENTER)
            return
        if(len(self.password_text.get()) < 5):
            error = Label(self, text="Errore: password troppo corta.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.65, anchor=CENTER)
            return
        if(self.conferma_password_text.get() != self.password_text.get()):
            error = Label(self, text="Errore: le password non coincidono", font=(18), fg="red")
            error.place(relx=0.5, rely=0.65, anchor=CENTER)
            return
        
        users = self.db.read_user("username", "username", self.username_text.get())
        if(len(users) != 0):
            error = Label(self, text="Esiste già un utente con qesto username.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.65, anchor=CENTER)
            return
        
        self.db.insert_user(self.username_text.get(), self.nome_text.get(), self.cognome_text.get(), self.password_text.get())
        self.controller.show_frame(Home)