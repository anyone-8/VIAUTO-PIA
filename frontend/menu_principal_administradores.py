#clase para cerar el menu pricipal
from backend.CRUD_convenios import Convenios
from frontend.gui_autos_v2 import Menu_gui_autos
import customtkinter as ctk

class principal_administradores(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.convenios = Convenios()

        self.opciones()

    def opciones(self):
        self.__opciones = {}

        self.__opciones["place"] = {}

        e_place = self.__opciones["place"]

        e_place["boton_autos"] = ctk.CTkButton(self, text="Catalogo de autos", width=80, height=80, command=self.menu_autos)

        e_place["boton_autos"].place(relx=0.20, rely=0.20, anchor="nw")


    def menu_autos(self):
        self.ocultar_opciones()

        self.gui_menu_autos = Menu_gui_autos(master=self, width=1500, height=1000)

        self.gui_menu_autos.place(relx=0.5, rely=0.5, anchor="center")

    def ocultar_opciones(self):
        for widget in self.__opciones["place"].values():
            widget.place_forget()



    