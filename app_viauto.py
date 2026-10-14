#este es el archivo que correra todo lo demas.
import customtkinter as ctk
from frontend.pantalla_inicio_sesion import Inicio_sesion
from frontend.menu_principal_administradores import principal_administradores

#definimos la pantalla de incio
class app_viauto(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.incio_de_sesion()
        
    def incio_de_sesion(self):
        self.geometry("1000x500")
        self.title("Incio de Sesion")

        self.menu_incio_sesion = Inicio_sesion(master=self, finalizar=self.iniciador_menu_principal, width=1000, height=500)
        self.menu_incio_sesion.place(relx=0.5, rely=0.5, anchor="center")

    def iniciador_menu_principal(self):
        self.geometry("1500x1000")
        if self.menu_incio_sesion.acceso == "usuario":
            self.menu_principa_usuarios()
        elif self.menu_incio_sesion.acceso == "administradores":
            self.title("Menu Administradores")
            self.menu_principal_administradores()

    def menu_principa_usuarios(self):
        pass

    def menu_principal_administradores(self):
        self.menu_administradordes = principal_administradores(master=self, width=1500, height=1000)
        self.menu_administradordes.place(relx=0.5, rely=0.5, anchor="center")




        

if __name__ == "__main__":
    app = app_viauto()
    app.mainloop()
        

