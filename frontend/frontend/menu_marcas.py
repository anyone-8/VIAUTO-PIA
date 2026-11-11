#clase para añadir  marca
import customtkinter as ctk
from backend.CRUD_convenios import Convenios

class menu_marcas(ctk.CTkFrame):
    def __init__(self, master, menu_anterior, **kwargs):
        super().__init__(master, **kwargs)

        self.__convenios = Convenios()

        self.opciones = menu_anterior

        self.__datos = self.__convenios.data

        self.__marcas = [marca for marca in self.__datos.keys()]

        self.__estado_añadir = False

        self.gui_menu_marcas()


    def gui_menu_marcas(self):
        for widget in self.winfo_children():
            widget.place_forget()

        if self.__estado_añadir == True:
            
            self.__convenios = Convenios()
            self.__datos = self.__convenios.data
            self.__marcas = [marca for marca in self.__datos.keys()]

            aviso = ctk.CTkLabel(self, text="Marca añadida con exito")
            aviso.place(relx=0.5, rely=0.235, anchor="center")

            self.__estado_añadir = False


        font1 = ctk.CTkFont(family="helvetica", size=18, weight="bold")

        titulo = ctk.CTkLabel(self, text="Marcas Registradas", font=font1)
        volver = ctk.CTkButton(self, text="volver", width=100, height=40, command=self.salir)
        contenedor = ctk.CTkScrollableFrame(self, width=500, height=500)
        añadir_marca = ctk.CTkButton(self, text="añadir", font=font1, width=500, height=40, command=self.añadir)

        titulo.place(relx=0.5, rely=0.2, anchor="center")
        contenedor.place(relx=0.5, rely=0.52, anchor="center")
        añadir_marca.place(relx=0.5, rely=0.82, anchor="center")
        volver.place(relx=0.2, rely=0.2, anchor="nw")

        for marca in self.__marcas:
            frame = ctk.CTkLabel(master=contenedor, text=marca)

            frame.pack(padx=5, pady=10)


    def añadir(self):
        for widget in self.winfo_children():
            widget.place_forget()

        self.__entrada = ctk.CTkEntry(self, width=300, height=40)
        boton_volver = ctk.CTkButton(self, text="volver", width=100, height=40, command=self.gui_menu_marcas)
        boton_añadir = ctk.CTkButton(self, text="añadir", width=300, height=40, command=self.añadir_crud)

        self.__entrada.place(relx=0.5, rely=0.45, anchor="center")
        boton_añadir.place(relx=0.5, rely=0.55, anchor="center")
        boton_volver.place(relx=0.2, rely=0.2, anchor="nw")
                                     
    def añadir_crud(self):
        marca = self.__entrada.get()

        if self.__convenios.añadir_marca(marca):
            self.__estado_añadir = True
            self.gui_menu_marcas()
            
        else:
            error = ctk.CTkLabel(self, text="la marca ya exite o no se pudo guardar")

            error.place(relx=0.5, rely=0.65, anchor="center")

    def salir(self):
        self.destroy()
        self.opciones()

