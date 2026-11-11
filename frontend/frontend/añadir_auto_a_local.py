#clase para añadir al inventario de locales un auto
import customtkinter as ctk
from backend.CRUD import Libro_Mayor
from backend.CRUD_convenios import Convenios
from PIL import Image

class Menu_Sutir_Local(ctk.CTkFrame):
    def __init__(self, master, menu_anterior, **kwargs):
        super().__init__(master, **kwargs)

        self.libro = Libro_Mayor()
        self.locales_dic = self.libro.data["locales"]
        self.locales = [local for local in self.libro.data["locales"].values()]
        self.codigos_locales = self.libro.data["directorios"]["D-locales"]
        self.convenios = Convenios()
        self.__data = self.convenios.data
        self.opciones = menu_anterior
        self.__paginacion = None
        self.__estado = False
        self.__texto_estado = "prueba"

        self.__pagina = 1

        self.__modelos = [ 
            modelo 
            for modelos in self.__data.values() 
            for modelo in modelos.keys() ]

        self.autos = [
            {**informacion, "marca": marca, "modelo": clave}
            for marca, modelos in self.__data.items()
            for clave, informacion in modelos.items()
            ]

        
        self.seleccionar_local()

    def seleccionar_local(self):
        for widget in self.winfo_children():
            widget.place_forget()

        font1 = ctk.CTkFont(family="Calibri", size=24, weight="bold")

        volver = ctk.CTkButton(self, text="volver", width=100, height=40, command=self.salir)
        titulo = ctk.CTkLabel(self, text="Locales disponibles", font=font1)
        contenedor = ctk.CTkScrollableFrame(self, width=500, height=500)

        contenedor.place(relx=0.5, rely=0.55, anchor="center")
        titulo.place(relx=0.5, rely=0.18, anchor="center")
        volver.place(relx=0.2, rely=0.2, anchor="nw")

        for id_local, local in self.locales_dic.items():
            i_local = local["nombre"]

            mostrar_local = ctk.CTkButton(master=contenedor, text=i_local, width=400, height=40, command=lambda n=id_local: self.seleccionar_auto(n))

            mostrar_local.pack(padx=4, pady=5)

    def seleccionar_auto(self, id_local):
        for widget in self.winfo_children():
            widget.place_forget()

        if self.__estado == True:
            texto = f"auto {self.__texto_estado} añadido con exito"
            estado = ctk.CTkLabel(self, text=texto)
            estado.place(relx=0.5, rely=0.6, anchor="center")
            self.__estado = False

        font1 = ctk.CTkFont(family="Calibri", size=26, weight="bold")
        font2 =ctk.CTkFont(family="Calibri", size=16, weight="bold")

        self._contenedor_autos = ctk.CTkFrame(self, width=1300, height=600, bg_color="gray")
        titulo = ctk.CTkLabel(self, text="Elije el auto a añadir", font=font1)
        boton_atras = ctk.CTkButton(self, text="←", font=font2, width=500, height=50, command=lambda: self.navegacion(-1, id_local))
        boton_adelante = ctk.CTkButton(self, text="→", font=font2, width=500, height=50, command=lambda: self.navegacion(1, id_local))
        boton_volver = ctk.CTkButton(self, text="regresar", font=font2, width=150, height=50,command=self.seleccionar_local)

        self._contenedor_autos.place(relx=0.5, rely=0.4, anchor="center")
        titulo.place(relx=0.5, rely=0.2, anchor="center")
        boton_atras.place(relx=0.49, rely=0.7, anchor="ne")
        boton_adelante.place(relx=0.51, rely=0.7, anchor="nw")
        boton_volver.place(relx=0.1, rely=0.2, anchor="nw")

        self.estructuracion_autos(self.__pagina, id_local)

        for i in range(5):
            self._contenedor_autos.grid_columnconfigure(i, weight=1, pad=10)

        for i in range(2):
            self._contenedor_autos.grid_rowconfigure(i, weight=1, pad=10)

    def navegacion(self, cambio, id_local):
        n_autos = len(self.__modelos)
        n_paginas = (n_autos - 1) // 5 + 1

        if cambio == None:
            cambio = 0

        if self.__pagina >= 1 and self.__pagina <= n_paginas:
            self.__pagina += cambio
        else:
            print("me valio madres y no sume")

        if self.__pagina <= 0:
            self.__pagina = 1

        if self.__pagina >= n_paginas + 1:
            self.__pagina = n_paginas

        self.estructuracion_autos(self.__pagina, id_local)

    def estructuracion_autos(self, pagina, id_local):
        for widget in self._contenedor_autos.winfo_children():
            widget.grid_forget()

 
        lim_inferior = 5*(pagina - 1)
        iteracion = 0

        if self.__paginacion in self.winfo_children():
            self.__paginacion.destroy()

        #calculamos las paginas totales nuevamente
        n_autos = len(self.__modelos)
        n_paginas = (n_autos - 1) // 5 + 1

        texto_paginacion = f"{self.__pagina} / {n_paginas}"
        self.__paginacion = ctk.CTkLabel(self, text=texto_paginacion)

        self.__paginacion.place(relx=0.5, rely=0.65, anchor="center")

        for i in range(lim_inferior, lim_inferior + 5):
            if i >= len(self.autos):
                break

            marca = self.autos[i]["marca"]
            modelo = self.autos[i]["modelo"]

            imagen = Image.open(f"datos/convenios/{marca}/{self.__data[marca][modelo]["imagen"]}")
            imagen_final = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(130, 130))
            informacion = f"{marca}\n {modelo}\n {self.__data[marca][modelo]["precio"]}"

            boton_auto = ctk.CTkButton(
                self._contenedor_autos, 
                text=informacion, 
                image=imagen_final,
                compound="top",
                anchor="center", 
                fg_color="transparent",
                border_spacing=10,
                width=200,
                height=230,
                command=lambda n = self.autos[i]: self.añadir_auto_a_local(n, id_local)
                )

            boton_auto.grid(row=0, column=iteracion, padx=10, pady=10, sticky="nsew")

            iteracion += 1

    def añadir_auto_a_local(self, auto, id_local):
        if self.convenios.auto_a_local(auto, id_local) == True:
            self.__estado = True
            print(f"auto: {auto["modelo"]}")
            self.__texto_estado = auto["modelo"]
            print(self.__texto_estado)
            self.seleccionar_auto(id_local)
        else:
            self.__texto_estado = "no"
            self.seleccionar_auto(id_local)
            
        
    def salir(self):
        self.destroy()
        self.opciones()
