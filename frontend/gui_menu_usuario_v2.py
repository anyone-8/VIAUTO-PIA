#clase actualizada de gui menu usuarios
import json
import customtkinter as ctk
from pathlib import Path
from PIL import Image
from backend.leer_locales import lectura_de_locales
from backend.CRUD_convenios import Convenios
from frontend.intento_de_amortizacion import SimuladorFinanciamiento
from backend.CRUD import Libro_Mayor

class Menu_Usuario(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.libro = Libro_Mayor()
        self.locales = self.libro.data["locales"]
        self.convenios = Convenios()
        self.__data = self.convenios.data

        
        

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

        

        self.general_mostrar_autos()

    def general_mostrar_autos(self):
        for widget in self.winfo_children():
            widget.place_forget()

        
        font1 = ctk.CTkFont(family="Calibri", size=26, weight="bold")
        font2 =ctk.CTkFont(family="Calibri", size=16, weight="bold")

        self._contenedor_autos = ctk.CTkFrame(self, width=1300, height=600, bg_color="gray")
        titulo = ctk.CTkLabel(self, text="Autos Convenidos", font=font1)
        filtro = ctk.CTkOptionMenu(self, width=300, height=30, values=["sin filtro", "por marca", "por precio"], font=font2, command=lambda choice: self.opciones_buscar(choice))
        boton_atras = ctk.CTkButton(self, text="←", font=font2, width=500, height=50, command=lambda: self.navegacion(-1))
        boton_adelante = ctk.CTkButton(self, text="→", font=font2, width=500, height=50, command=lambda: self.navegacion(1))
        

        self._contenedor_autos.place(relx=0.5, rely=0.4, anchor="center")
        titulo.place(relx=0.5, rely=0.2, anchor="center")
        filtro.place(relx=0.5, rely=0.25, anchor="center")
        boton_atras.place(relx=0.49, rely=0.7, anchor="ne")
        boton_adelante.place(relx=0.51, rely=0.7, anchor="nw")
       

        self.estructuracion_autos(1)

        for i in range(5):
            self._contenedor_autos.grid_columnconfigure(i, weight=1, pad=10)

        for i in range(2):
            self._contenedor_autos.grid_rowconfigure(i, weight=1, pad=10)

    def opciones_buscar(self, opcion):
        if opcion == "sin filtro":
            self.sin_filtro()
        elif opcion == "por marca":
            pass
        elif opcion == "por precio":
            pass

    def navegacion(self, cambio):
        print(f"el cambio fue: {cambio}")
        print(f"la pagina incialmente es: {self.__pagina}")
        
        n_autos = len(self.__modelos)
        n_paginas = (n_autos - 1) // 5 + 1

        print(f"Las paginas totales son: {n_paginas}")

        if cambio == None:
            cambio = 0

        if self.__pagina >= 1 and self.__pagina <= n_paginas:
            self.__pagina += cambio
        else:
            print("me valio madres y no sume")

        print(f"la pagina actual es: {self.__pagina}")

        if self.__pagina <= 0:
            self.__pagina = 1

        if self.__pagina >= n_paginas + 1:
            self.__pagina = n_paginas
            print(f"me vine por aqui en el if: {self.__pagina}, {n_paginas}")

        self.estructuracion_autos(self.__pagina)

    def estructuracion_autos(self, pagina):
        for widget in self._contenedor_autos.winfo_children():
            widget.grid_forget()


       
        
        lim_inferior = 5*(pagina - 1)
        lim_superior = 5*(pagina) - 1
        iteracion = 0

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
                command=lambda n = self.autos[i]: self.menu_autos_individual(n)
                )

            boton_auto.grid(row=0, column=iteracion, padx=10, pady=10, sticky="nsew")

            iteracion += 1


    def menu_autos_individual(self, auto):
        for widget in self.winfo_children():
            widget.place_forget()

        marca = auto["marca"]
        modelo = auto["modelo"]
        lista_coincidencias = lectura_de_locales(marca, modelo)

        
            
        

        datos = self.__data[marca][modelo]
        font1 = ctk.CTkFont(family="Calibri", size=24, weight="bold")

        imagen = Image.open(f"datos/convenios/{marca}/{datos["imagen"]}")

        imagen_final = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(300, 300))

        texto = f"""
        marca: {datos["marca"]}
        modelo: {datos["modelo"]}
        precio: {datos["precio"]}
        año de fabricacion: {datos["año_de_fabricacion"]}
        caballos de fuerza: {datos["caballos_de_fuerza"]}
        capacidad: {datos["capacidad"]}
        peso: {datos["peso"]}
        consumo conbinado: {datos["consumo_conbinado"]}
        dimensiones
            largo: {datos["dimensiones"]["largo"]}
            ancho: {datos["dimensiones"]["ancho"]}
            alto: {datos["dimensiones"]["alto"]}

        locales con existencias:
        {lista_coincidencias}
        """

        mostrar_imagen = ctk.CTkLabel(self, image=imagen_final, text="")
        datos_auto = ctk.CTkLabel(
            self, 
            text=texto,
            justify="left",
            font=font1
            )
        caracteristicas = ctk.CTkTextbox(self, width=300, height=250, activate_scrollbars=True)

        simulacion = ctk.CTkButton(self, text="simulacion de cotizacion", width=200, height=70, command=lambda n = datos["precio"] :self.simular_pagos(n))
        boton_regresar = ctk.CTkButton(self, text="volver", width=10, height=40, command=self.general_mostrar_autos)

        caracteristicas.configure(state="normal")
        caracteristicas.insert("1.0", datos["descripcion"])
        caracteristicas.configure(state="disabled")

        mostrar_imagen.place(relx=0.2, rely=0.2, anchor="nw")
        datos_auto.place(relx=0.4, rely=0.2, anchor="nw")
        caracteristicas.place(relx=0.2, rely=0.53, anchor="nw")
        boton_regresar.place(relx=0.7, rely=0.2, anchor="nw")
        simulacion.place(relx=0.6, rely=0.7, anchor="nw")


    def simular_pagos(self, precio):
        self.__cotizacion = SimuladorFinanciamiento(master=self, precio_fijo=precio)