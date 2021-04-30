from tkinter import *
import LoginPage
import HomePage
from DBManager.DB import Database

class Profilo(Frame):
    def __init__(self, parent, controller, username):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.username = username
        self.db = Database()
        self.create_widgets()
    
    def create_widgets(self):
        self.nome_label = Label(self, text="I tuoi dati.", font=("bold", 25), pady=20)
        self.nome_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        isOn = NORMAL

        self.nome_label = Label(self, text="Nome:", font=(18), pady=20)
        self.nome_label.place(relx=0.3, rely=0.2, anchor=CENTER)
        self.nome_text = StringVar()
        self.nome_textbox = Entry(self, width=20, textvariable=self.nome_text)
        self.nome_textbox.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.nome_textbox.insert(0, self.db.read_user("nome", "username", self.username)[0][0])

        self.cognome_label = Label(self, text="Cognome:", font=(18), pady=20)
        self.cognome_label.place(relx=0.3, rely=0.3, anchor=CENTER)
        self.cognome_text = StringVar()
        self.cognome_textbox = Entry(self, width=20, textvariable=self.cognome_text)
        self.cognome_textbox.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.cognome_textbox.insert(0, self.db.read_user("cognome", "username", self.username)[0][0])

        self.username_label = Label(self, text="Username:", font=(18), pady=20)
        self.username_label.place(relx=0.3, rely=0.4, anchor=CENTER)
        self.username_text = StringVar()
        self.username_textbox = Entry(self, width=20, textvariable=self.username_text)
        self.username_textbox.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.username_textbox.insert(0, self.username)

        self.modifica_button = Button(self, text="Modifica i tuoi dati", font=(18), width=10, command=self.modifica)
        self.modifica_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.modifica_button = Button(self, text="Modifica password", font=(18), width=10, command=self.modifica_password)
        self.modifica_button.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.indietro_button = Button(self, text="Indietro", font=(18), width=10, command=lambda : self.controller.show_frame(HomePage.Home, self.username))
        self.indietro_button.place(relx=0.5, rely=0.95, anchor=CENTER)

    def modifica(self):
        users = self.db.read_user("username", "username", self.username_text.get())
        if(len(users) != 0 and users[0][0] != self.username):
            error = Label(self, text="Esiste già un utente con questo username.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.45, anchor=CENTER)
            return
        self.db.update_user(self.username, self.username_text.get(), self.nome_text.get(), self.cognome_text.get(), self.db.read_user("password", "username", self.username)[0][0])
        self.username = self.username_text.get()
        error = Label(self, text="Modifiche effettuate correttamente", font=(18), fg="green")
        error.place(relx=0.5, rely=0.45, anchor=CENTER)

    def modifica_password(self):

        def mod():
            password = self.db.read_user("password", "username", self.username)[0]
            if(password[0] != self.vecchia_password_text.get()):
                error = Label(self, text="Vecchia password errata", font=(18), fg="red")
                error.place(relx=0.5, rely=0.8, anchor=CENTER)
                return
            if(len(self.nuova_password_text.get()) < 5):
                error = Label(self, text="Errore: password troppo corta.", font=(18), fg="red")
                error.place(relx=0.5, rely=0.8, anchor=CENTER)
                return
            if(self.conferma_nuova_password_text.get() != self.nuova_password_text.get()):
                error = Label(self, text="Errore: le password non coincidono", font=(18), fg="red")
                error.place(relx=0.5, rely=0.8, anchor=CENTER)
                return
            self.db.update_user(self.username, self.username, self.db.read_user("nome", "username", self.username)[0][0], \
                                self.db.read_user("cognome", "username", self.username)[0][0], self.nuova_password_text.get())
            error = Label(self, text="Modifiche effettuate correttamente", font=(18), fg="green")
            error.place(relx=0.5, rely=0.8, anchor=CENTER)
            

        self.vecchia_password_label = Label(self, text="Vecchia password:", font=(18), pady=20)
        self.vecchia_password_label.place(relx=0.3, rely=0.65, anchor=CENTER)
        self.vecchia_password_text = StringVar()
        self.vecchia_password_textbox = Entry(self, width=20, textvariable=self.vecchia_password_text, show="*")
        self.vecchia_password_textbox.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.nuova_password_label = Label(self, text="Nuova password:", font=(18), pady=20)
        self.nuova_password_label.place(relx=0.3, rely=0.7, anchor=CENTER)
        self.nuova_password_text = StringVar()
        self.nuova_password_textbox = Entry(self, width=20, textvariable=self.nuova_password_text, show="*")
        self.nuova_password_textbox.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.conferma_nuova_password_label = Label(self, text="Conferma nuova password:", font=(18), pady=20)
        self.conferma_nuova_password_label.place(relx=0.3, rely=0.75, anchor=CENTER)
        self.conferma_nuova_password_text = StringVar()
        self.conferma_nuova_password_textbox = Entry(self, width=20, textvariable=self.conferma_nuova_password_text, show="*")
        self.conferma_nuova_password_textbox.place(relx=0.5, rely=0.75, anchor=CENTER)

        self.modifica_button = Button(self, text="Cambia password", font=(18), width=10, command=mod)
        self.modifica_button.place(relx=0.5, rely=0.85, anchor=CENTER)