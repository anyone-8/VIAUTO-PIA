#clase para cerar el menu pricipal
from backend.CRUD_convenios import Convenios
from frontend.gui_autos_v2 import Menu_gui_autos
from frontend.menu_marcas import menu_marcas
from frontend.añadir_auto_a_local import Menu_Sutir_Local
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

        e_place["boton_autos"] = ctk.CTkButton(self, text="Catalogo de autos", width=150, height=100, command=self.menu_autos)
        e_place["boton_añadir_marca"] = ctk.CTkButton(self, text="añadir marca\n a convenios", width=150, height=100, command=self.menu_añadir_marca)
        e_place["boton_añadir_a_local"] = ctk.CTkButton(self, text="añadir auto\n a local", width=150, height=100, command=self.añadir_carro_local)

        e_place["boton_autos"].place(relx=0.20, rely=0.20, anchor="nw")
        e_place["boton_añadir_marca"].place(relx=0.4, rely=0.2, anchor="nw")
        e_place["boton_añadir_a_local"].place(relx=0.6, rely=0.2, anchor="nw")


    def menu_autos(self):
        self.ocultar_opciones()

        self.gui_menu_autos = Menu_gui_autos(master=self, menu_anterior=self.opciones, width=1500, height=1000)

        self.gui_menu_autos.place(relx=0.5, rely=0.5, anchor="center")

    def menu_añadir_marca(self):
        self.ocultar_opciones()

        self.gui_menu_añadir_marca = menu_marcas(master=self, menu_anterior=self.opciones, width=1500, height=1000)

        self.gui_menu_añadir_marca.place(relx=0.5, rely=0.5, anchor="center")

    def añadir_carro_local(self):
        self.ocultar_opciones()

        self.gui_menu_añadir_auto_a_local = Menu_Sutir_Local(master=self, menu_anterior=self.opciones, width=1500, height=1000)

        self.gui_menu_añadir_auto_a_local.place(relx=0.5, rely=0.5, anchor="center")

    def ocultar_opciones(self):
        for widget in self.__opciones["place"].values():
            widget.place_forget()



    