from tkinter import *
from LoginPage import Login
from RegistrazionePage import Registrazione
from HomePage import Home
from ProfiloPage import Profilo
from CompanyPage import Company
from CreateCompanyPage import CreateCompany

class Main(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x800")
        self.title("Nome App")
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
  
        self.frames = {}
        self.frame_names = [Login, Registrazione, Home, Profilo, Company, CreateCompany]
        self.frames_dinamici = [Home , Profilo, Company, CreateCompany]
  
        self.show_frame(Login)

    def show_frame(self, F, username=None, name=None):
        try:
            frame = self.frames[F]
            self.frames[F].destroy()
            if(F in self.frames_dinamici):
                if(F == Company):
                    self.frames[F] = F(self.container, self, username, name)    
                else:
                    self.frames[F] = F(self.container, self, username)
                frame = self.frames[F]
            else:
                self.frames[F] = F(self.container, self)
                frame = self.frames[F]
        except KeyError:
            if (F in self.frames_dinamici):
                if(F == Company):
                    frame = F(self.container, self, username, name)
                else:
                    frame = F(self.container, self, username)
                self.frames[F] = frame
            else:
                frame = F(self.container, self)
                self.frames[F] = frame
        for f in self.frame_names:
            if f != F:
                try:
                    self.frames[f].pack_forget()
                except KeyError:
                    continue
        frame.pack(fill="both", expand=True)
        frame.tkraise()

def main():
    app = Main()
    app.mainloop()

if __name__ == "__main__":
    main()