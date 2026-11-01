#clase para añadir  marca
import customtkinter as ctk
from backend.CRUD_convenios import Convenios

class menu_marcas(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.__convenios = Convenios()

        self.__datos = self.__convenios.data

        self.__marcas = [marca for marca in self.__datos.keys()]

        self.gui_menu_marcas(self.__marcas)


    def gui_menu_marcas(self, marcas):
        font1 = ctk.CTkFont(family="helvetica", size=28, weight="bold")

        titulo = ctk.CTkLabel(self, text="Marcas Registradas", font=font1)
        contenedor = ctk.CTkScrollableFrame(self, width=500, height=500)
        añadir_marca = ctk.CTkButton(self, text="añadir", font=font1, width=500, height=40, command=self.añadir)

        titulo.place(relx=0.5, rely=0.2, anchor="center")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")
        añadir_marca.place(relx=0.5, rely=0.8, anchor="center")

        for marca in self.__marcas:
            frame = ctk.CTkLabel(master=contenedor, text=marca)

            frame.pack(padx=5, pady=10)


    def añadir(self):
        for widget in self.winfo_children():
            widget.place_forget()

        self.__entrada = ctk.CTkEntry(self, width=300, height=40)
        boton_añadir = ctk.CTkButton(self, text="añadir", width=300, height=40, command=self.añadir_crud)

        self.__entrada.place(relx=0.5, rely=0.45, anchor="center")
        boton_añadir.place(relx=0.5, rely=0.55, anchor="center")
                                     
    def añadir_crud(self):
        marca = self.__entrada.get()

        self.__convenios.añadir_marca(marca)



