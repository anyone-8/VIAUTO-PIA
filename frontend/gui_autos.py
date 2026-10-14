#clase para el menu de autos de el menu princiapl
from backend.CRUD import Libro_Mayor
from backend.CRUD_convenios import Convenios
import customtkinter as ctk
from PIL import Image

class Menu_gui_autos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.libro = Libro_Mayor()
        self.locales = self.libro.data["locales"]
        self.convenios = Convenios()
        self.autos = self.convenios.data

        self.__modelos = [
            modelo
            for modelos in self.autos.values()
            for modelo in modelos.keys()
        ]


        self.general_mostrar_autos()

    def general_mostrar_autos(self):
        font1 = ctk.CTkFont(family="Calibri", size=26, weight="bold")
        font2 =ctk.CTkFont(family="Calibri", size=16, weight="bold")

        self._contenedor_autos = ctk.CTkFrame(self, width=1300, height=600, bg_color="gray")
        titulo = ctk.CTkLabel(self, text="Autos Convenidos", font=font1)
        filtro = ctk.CTkOptionMenu(self, width=300, height=30, values=["sin filtro", "por marca", "por precio"], font=font2, command=lambda choice: self.opciones_buscar(choice))
        boton_atras = ctk.CTkButton(self, text="←", font=font2, width=500, height=50, command=lambda: self.navegacion(-1))
        boton_adelante = ctk.CTkButton(self, text="→", font=font2, width=500, height=50, command=lambda: self.navegacion(1))
        boton_volver = ctk.CTkButton(self, text="regresar", font=font2, width=150, height=50)

        self._contenedor_autos.place(relx=0.5, rely=0.4, anchor="center")
        titulo.place(relx=0.5, rely=0.2, anchor="center")
        filtro.place(relx=0.5, rely=0.25, anchor="center")
        boton_atras.place(relx=0.47, rely=0.7, anchor="ne")
        boton_adelante.place(relx=0.53, rely=0.7, anchor="nw")
        boton_volver.place(relx=0.1, rely=0.2, anchor="nw")

    def opciones_buscar(self, opcion):
        if opcion == "sin filtro":
            self.sin_filtro()
        elif opcion == "por marca":
            pass
        elif opcion == "por precio":
            pass

    def navegacion(self, cambio):
        n_autos = len(self.__modelos)
        n_paginas = n_autos // 10

        if cambio < 1:
            cambio = 1
        elif cambio > n_paginas:
            cambio = n_paginas
        elif cambio == None:
            cambio = 1

        if cambio >= 2 and cambio <= n_paginas - 1:
            pagina += cambio

        lim_inferior = 10(n_paginas - 1) + 1
        lim_superior = 10(n_paginas)

        for i in range(lim_inferior, lim_superior/2):
            modelo_auto = ctk.CTkFrame(master=self._contenedor_autos, width=150, height=150)
            seleccionar = ctk.CTkButton()
            nombre_modelo = ctk.CTkLabel()
            for valores in self.autos.values:
                ruta_imagen = valores[self.__modelos[i]]["imagen"]
            #imagen = Image.

        for i in range(lim_superior/2 + 1, lim_superior):
            pass
        #lim inferior (10(n - 1) + 1)
        #lim superiro 10(n)

    def sin_filtro(self):
        pass
        






