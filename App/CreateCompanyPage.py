from tkinter import *
from tkinter import ttk
import tkcalendar
import HomePage
from DBManager.DB import Database

class CreateCompany(Frame):
    def __init__(self, parent, controller, username):
        super().__init__(parent)
        self.controller = controller
        self.username = username
        self.db = Database()
        self.create_widgets()
    
    def create_widgets(self):
        self.register_label = Label(self, text="Aggiungi un'azienda", font=("bold", 25), pady=20)
        self.register_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.nome_label = Label(self, text="Nome:", font=(18))
        self.nome_label.place(relx=0.3, rely=0.2, anchor=CENTER)
        self.nome_text = StringVar()
        self.nome_textbox = Entry(self, width=20, textvariable=self.nome_text)
        self.nome_textbox.place(relx=0.5, rely=0.2, anchor=CENTER)
        
        markets = ['Other','Software','Curated Web','Analytics','E-Commerce','Games','Semiconductors','Clean Technology','Finance','Mobile','Biotechnology','Search','Advertising','Security','Health Care','Enterprise Software','Social Media','Messaging','Web Hosting','Hardware + Software','Education']
        self.market_label = Label(self, text="Settore:", font=(18))
        self.market_label.place(relx=0.3, rely=0.3, anchor=CENTER)
        self.market_text = StringVar()
        self.market_combobox = ttk.Combobox(self, values=markets)
        self.market_combobox.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.total_investment_label = Label(self, text="Totale fondi ricevuti:", font=(18))
        self.total_investment_label.place(relx=0.3, rely=0.4, anchor=CENTER)
        self.total_investment_text = StringVar()
        self.total_investment_textbox = Entry(self, width=20, textvariable=self.total_investment_text)
        self.total_investment_textbox.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.funding_rounds_label = Label(self, text="Numero investimenti ricevuti:", font=(18))
        self.funding_rounds_label.place(relx=0.3, rely=0.5, anchor=CENTER)
        self.funding_rounds_text = StringVar()
        self.funding_rounds_textbox = Entry(self, width=20, textvariable=self.funding_rounds_text)
        self.funding_rounds_textbox.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.founded_at_label = Label(self, text="Fondata nel:", font=(18))
        self.founded_at_label.place(relx=0.3, rely=0.6, anchor=CENTER)
        self.founded_at_cal = tkcalendar.DateEntry(self, fg="black")
        self.founded_at_cal.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.first_funding_at_label = Label(self, text="Data primo investimento:", font=(18))
        self.first_funding_at_label.place(relx=0.3, rely=0.7, anchor=CENTER)
        self.first_funding_at_cal = tkcalendar.DateEntry(self, fg="black")
        self.first_funding_at_cal.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.last_funding_at_label = Label(self, text="Data ultimo investimento:", font=(18))
        self.last_funding_at_label.place(relx=0.3, rely=0.8, anchor=CENTER)
        self.last_funding_at_cal = tkcalendar.DateEntry(self, fg="black")
        self.last_funding_at_cal.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.inserimento_button = Button(self, text="Inserisci azienda", font=(18), width=20, command=lambda : self.inserisci())
        self.inserimento_button.place(relx=0.5, rely=0.9, anchor=CENTER)

        self.indietro_button = Button(self, text="Indietro", font=(18), width=10, command=lambda : self.controller.show_frame(HomePage.Home, self.username))
        self.indietro_button.place(relx=0.5, rely=0.95, anchor=CENTER)

    def inserisci(self):
        if(len(self.nome_text.get()) < 3):
            error = Label(self, text="Errore: nome troppo corto.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.85, anchor=CENTER)
            return
        if(len(self.market_combobox.get()) == 0):
            error = Label(self, text="Errore: selezionare un settore.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.85, anchor=CENTER)
            return
        try:
            float(self.total_investment_text.get())
        except:
            error = Label(self, text="Errore: il totale dei fondi ricevuti deve essere numerico.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.85, anchor=CENTER)
            return
        try:
            int(self.funding_rounds_text.get())
        except:
            error = Label(self, text="Errore: il numero di investimenti ricevuti deve essere un numero intero.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.85, anchor=CENTER)
            return

        companies = self.db.read_company("name", "name", self.nome_text.get())
        if(len(companies) != 0):
            error = Label(self, text="Esiste già un'azienda con qesto username.", font=(18), fg="red")
            error.place(relx=0.5, rely=0.85, anchor=CENTER)
            return
        
        self.db.insert_company(self.nome_text.get(), self.market_combobox.get(), float(self.total_investment_text.get()), int(self.funding_rounds_text.get()), self.founded_at_cal.get_date(), self.first_funding_at_cal.get_date(), self.last_funding_at_cal.get_date())
        self.controller.show_frame(HomePage.Home, self.username)