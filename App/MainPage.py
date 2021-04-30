from tkinter import *
from LoginPage import Login
from RegistrazionePage import Registrazione
from HomePage import Home
from ProfiloPage import Profilo

class Main(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x800")
        self.title("Nome App")
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
  
        self.frames = {} 
        self.frame_names = [Login, Registrazione, Home, Profilo]
  
        self.show_frame(Login)

    def show_frame(self, F, username=None):
        try:
            frame = self.frames[F]
            if(F == Home or F == Profilo):
                self.frames[F].username = username
                frame = self.frames[F]
        except KeyError:
            if (F == Home or F == Profilo):
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

app = Main()
app.mainloop()