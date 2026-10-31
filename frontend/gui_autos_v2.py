#gui autos mejorado
from backend.CRUD import Libro_Mayor
from backend.CRUD_convenios import Convenios
from pathlib import Path
import customtkinter as ctk
from PIL import Image

class Menu_gui_autos(ctk.CTkFrame):
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
        font1 = ctk.CTkFont(family="Calibri", size=26, weight="bold")
        font2 =ctk.CTkFont(family="Calibri", size=16, weight="bold")

        self._contenedor_autos = ctk.CTkFrame(self, width=1300, height=600, bg_color="gray")
        titulo = ctk.CTkLabel(self, text="Autos Convenidos", font=font1)
        filtro = ctk.CTkOptionMenu(self, width=300, height=30, values=["sin filtro", "por marca", "por precio"], font=font2, command=lambda choice: self.opciones_buscar(choice))
        boton_atras = ctk.CTkButton(self, text="←", font=font2, width=500, height=50, command=lambda: self.navegacion(-1))
        boton_adelante = ctk.CTkButton(self, text="→", font=font2, width=500, height=50, command=lambda: self.navegacion(1))
        boton_volver = ctk.CTkButton(self, text="regresar", font=font2, width=150, height=50)
        boton_añadir = ctk.CTkButton(self, text="añadir auto", font=font2, width=1000, height=50, command=self.seleccion_añadir_auto)

        self._contenedor_autos.place(relx=0.5, rely=0.4, anchor="center")
        titulo.place(relx=0.5, rely=0.2, anchor="center")
        filtro.place(relx=0.5, rely=0.25, anchor="center")
        boton_atras.place(relx=0.49, rely=0.7, anchor="ne")
        boton_adelante.place(relx=0.51, rely=0.7, anchor="nw")
        boton_volver.place(relx=0.1, rely=0.2, anchor="nw")
        boton_añadir.place(relx=0.5, rely=0.8, anchor="center")

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

        if cambio == None:
            cambio = 0

        if self.__pagina >= 1 and self.__pagina <= n_paginas:
            self.__pagina += cambio
        else:
            print("me valio madres y no sume")

        print(f"la pagina actual es: {self.__pagina}")

        if self.__pagina == 0:
            self.__pagina = 1

        self.estructuracion_autos(self.__pagina)

    def estructuracion_autos(self, pagina):
        for widget in self._contenedor_autos.winfo_children():
            widget.grid_forget()

        print(f"la pagina actual es: {pagina}")
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


    def menu_autos_individual(self, dic):
        pass

    def seleccion_añadir_auto(self):
        for widget in self.winfo_children():
            widget.place_forget()

        font1 = ctk.CTkFont(family="helvetica", size=18, weight="bold")

        titulo = ctk.CTkLabel(self, text="Seleccione una marca", font=font1)
        frame_marcas = ctk.CTkScrollableFrame(self, width=600, height=500)

        titulo.place(relx=0.5, rely=0.2, anchor="center")
        frame_marcas.place(relx=0.5, rely=0.5, anchor="center")

        for marca in self.__data.keys():
            opcion = ctk.CTkButton(frame_marcas, text=marca, width=500, height=30, command=lambda n = marca:self.menu_añadir_auto(n))

            opcion.pack(padx=15, pady=20)



    def menu_añadir_auto(self, marca):
        for widget in self.winfo_children():
            widget.place_forget()

        validador_numero = (self.register(lambda text: text == "" or text.replace(".", "", 1).isdigit()), "%P")

        font1 = ctk.CTkFont(family="helvetica", size=18, weight="bold")

        titulo = ctk.CTkLabel(self, text=f"Añadir auto para la marca {marca}", font=font1)


        self.__modelo_entrada = ctk.CTkEntry(self, width=250, height=30)
        self.__precio_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__año_fabricacion_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__caballos_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__capacidad_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__peso_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__consumo_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__largo_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__ancho_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__alto_entrada = ctk.CTkEntry(self, width=250, height=30, validate="key", validatecommand=validador_numero)
        self.__descripcion_entrada = ctk.CTkTextbox(self, width=300, height=150, activate_scrollbars=True)
        imagen_entrada = ctk.CTkButton(self, text="subir imagen", font=font1, width=200, height=50, command=self.subir_imagen)

        modelo_texto = ctk.CTkLabel(self, text="modelo", font=font1)
        precio_texto = ctk.CTkLabel(self, text="precio", font=font1)
        año_fabricacion_texto = ctk.CTkLabel(self, text="año de fabricacion", font=font1)
        caballos_texto = ctk.CTkLabel(self, text="caballos de fuerza", font=font1)
        capacidad_texto = ctk.CTkLabel(self, text="capacidad", font=font1)
        peso_texto = ctk.CTkLabel(self, text="peso", font=font1)
        consumo_texto = ctk.CTkLabel(self, text="consumo", font=font1)
        largo_texto = ctk.CTkLabel(self, text="largo", font=font1)
        ancho_texto = ctk.CTkLabel(self, text="ancho", font=font1)
        alto_texto = ctk.CTkLabel(self, text="alto", font=font1)
        descripcion_texto = ctk.CTkLabel(self, text="descripcion", font=font1)
        imagen_texto = ctk.CTkLabel(self, text="imagen", font=font1)

        subir_datos = ctk.CTkButton(self, text="agregar", font=font1, width=200, height=50, command=lambda: self.subir_auto(marca))

        modelo_texto.place(relx=0.23, rely=0.2, anchor="nw")
        self.__modelo_entrada.place(relx=0.23, rely=0.23, anchor="nw")
        precio_texto.place(relx=0.23, rely=0.26, anchor="nw")
        self.__precio_entrada.place(relx=0.23, rely=0.29, anchor="nw")
        año_fabricacion_texto.place(relx=0.23, rely=0.32, anchor="nw")
        self.__año_fabricacion_entrada.place(relx=0.23, rely=0.35, anchor="nw")
        caballos_texto.place(relx=0.23, rely=0.38, anchor="nw")
        self.__caballos_entrada.place(relx=0.23, rely=0.41, anchor="nw")
        capacidad_texto.place(relx=0.23, rely=0.44, anchor="nw")
        self.__capacidad_entrada.place(relx=0.23, rely=0.47, anchor="nw")
        peso_texto.place(relx=0.23, rely=0.50, anchor="nw")
        self.__peso_entrada.place(relx=0.23, rely=0.53, anchor="nw")
        consumo_texto.place(relx=0.23, rely=0.56, anchor="nw")
        self.__consumo_entrada.place(relx=0.23, rely=0.59, anchor="nw")
        largo_texto.place(relx=0.23, rely=0.62, anchor="nw")
        self.__largo_entrada.place(relx=0.23, rely=0.65, anchor="nw")
        ancho_texto.place(relx=0.23, rely=0.68, anchor="nw")
        self.__ancho_entrada.place(relx=0.23, rely=0.71, anchor="nw")
        alto_texto.place(relx=0.23, rely=0.74, anchor="nw")
        self.__alto_entrada.place(relx=0.23, rely=0.77, anchor="nw")
        descripcion_texto.place(relx=0.63, rely=0.2, anchor="nw")
        self.__descripcion_entrada.place(relx=0.63, rely=0.23, anchor="nw")
        imagen_texto.place(relx=0.63, rely=0.40, anchor="nw")
        imagen_entrada.place(relx=0.63, rely=0.67, anchor="nw")
        subir_datos.place(relx=0.63, rely=0.74, anchor="nw")


    def subir_imagen(self):
        self._archivo = ctk.filedialog.askopenfilename(title="selecciona una iamgen", filetypes=[("Imagenes jpg", "*.jpg")])

        if self._archivo:
            imagen_subida = Image.open(self._archivo)
            imagen_final = ctk.CTkImage(light_image=imagen_subida, dark_image=imagen_subida, size=(200, 200))
            mostrar_imagen = ctk.CTkLabel(self, image=imagen_final, text="")

            mostrar_imagen.place(relx=0.63, rely=0.45, anchor="nw")

    def subir_auto(self, marca):
        modelo = self.__modelo_entrada.get()
        precio = self.__precio_entrada.get()
        año_fabricacion = self.__año_fabricacion_entrada.get()
        caballos = self.__caballos_entrada.get()
        capacidad = self.__capacidad_entrada.get()
        peso = self.__peso_entrada.get()
        consumo = self.__consumo_entrada.get()
        largo = self.__largo_entrada.get()
        ancho = self.__ancho_entrada.get()
        alto = self.__alto_entrada.get()
        descripcion = self.__descripcion_entrada.get("1.0", "end")
        imagen = self._archivo

        coche = {
            "marca" : marca,
            "modelo": modelo,
            "precio" : precio,
            "año_de_fabricacion" : año_fabricacion,
            "caballos_de_fuerza" : caballos,
            "capacidad" : capacidad,
            "peso" : peso,
            "consumo_conbinado" : consumo,
            "dimensiones" : {
                "largo" : largo,
                "ancho" : ancho,
                "alto" : alto
            },
            "descripcion" : descripcion,
            "imagen" : f"{modelo}.jpg"
        }

        self.convenios.añadir_modelo(coche, imagen)

        

        
        
