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
        self.nome_label = Label(self, text="Azienda:\t" + self.name, font=("bold", 25))
        self.nome_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.market_label = Label(self, text="Settore:\t" + self.db.read_company("market", "name", self.name)[0][0], font=("bold", 25))
        self.market_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.total_investment_label = Label(self, text="Totale fondi ricevuti:\t" + str(self.db.read_company("total_investment", "name", self.name)[0][0]) + " $", font=("bold", 25))
        self.total_investment_label.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.funding_rounds_label = Label(self, text="Numero investimenti ricevuti:\t" + str(self.db.read_company("funding_rounds", "name", self.name)[0][0]), font=("bold", 25))
        self.funding_rounds_label.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.founded_at_label = Label(self, text="Fondata il:\t" + str(self.db.read_company("founded_at", "name", self.name)[0][0]), font=("bold", 25))
        self.founded_at_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.first_funding_at_label = Label(self, text="Data primo investimento:\t" + str(self.db.read_company("first_funding_at", "name", self.name)[0][0]), font=("bold", 25))
        self.first_funding_at_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.last_funding_at_label = Label(self, text="Data ultimo investimento:\t" + str(self.db.read_company("last_funding_at", "name", self.name)[0][0]), font=("bold", 25))
        self.last_funding_at_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.indietro_button = Button(self, text="Indietro", font=(18), width=10, command=lambda : self.controller.show_frame(HomePage.Home, self.username))
        self.indietro_button.place(relx=0.5, rely=0.9, anchor=NE)

