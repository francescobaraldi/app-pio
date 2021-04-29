from tkinter import *
from LoginPage import Login
from RegistrazionePage import Registrazione

class Main(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x800")
        self.title("Nome App")
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
  
        self.frames = {} 
        self.frame_names = [Login, Registrazione]
        for F in self.frame_names:
            frame = F(self.container, self)
            self.frames[F] = frame
  
        self.show_frame(Login)


    def show_frame(self, F):
        frame = self.frames[F]
        for f in self.frame_names:
            if f != F:
                self.frames[f].pack_forget()
        frame.pack(fill="both", expand=True)
        frame.tkraise()

app = Main()
app.mainloop()