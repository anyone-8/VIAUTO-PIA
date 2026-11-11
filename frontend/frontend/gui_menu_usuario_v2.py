#clase actualizada de gui menu usuarios
#se exportan las clases que se utilizan en el proyecto
import customtkinter as ctk
from PIL import Image
from backend.leer_locales import lectura_de_locales
from backend.CRUD_convenios import Convenios
from frontend.intento_de_amortizacion import SimuladorFinanciamiento
from backend.CRUD import Libro_Mayor

class Menu_Usuario(ctk.CTkFrame):

    def __init__(self, master, inicio_sesion, **kwargs):
        super().__init__(master, **kwargs)

        #se llaman y crean elementos que se utilizaran durante todo el menu o para agilizarlo
        self.libro = Libro_Mayor()
        self.locales = self.libro.data["locales"]
        self.convenios = Convenios()
        self.__data = self.convenios.data
        self.__sesion = inicio_sesion
        self.__paginacion = None
        
        

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

        
        #se inicia el bucle del programa
        self.general_mostrar_autos()

    def general_mostrar_autos(self):
        for widget in self.winfo_children():
            widget.place_forget()

        
        font1 = ctk.CTkFont(family="Calibri", size=26, weight="bold")
        font2 =ctk.CTkFont(family="Calibri", size=16, weight="bold")

        #aqui se crea el contenedor para poder mostrar los autos en el menu
        self._contenedor_autos = ctk.CTkFrame(self, width=1300, height=600, bg_color="gray")
        titulo = ctk.CTkLabel(self, text="Autos Convenidos", font=font1)
        aviso = ctk.CTkLabel(self, text="Enganche del 10% y tasa del 12% por año en todos los planes", font=font2)
        sesion = ctk.CTkButton(self, text="cambiar de sesion", width=100, height=40, command=self.cambiar_de_sesion)
        
        boton_atras = ctk.CTkButton(self, text="←", font=font2, width=500, height=50, command=lambda: self.navegacion(-1))
        boton_adelante = ctk.CTkButton(self, text="→", font=font2, width=500, height=50, command=lambda: self.navegacion(1))
        
        #se muestran los widgets
        self._contenedor_autos.place(relx=0.5, rely=0.4, anchor="center")
        titulo.place(relx=0.5, rely=0.2, anchor="center")
        aviso.place(relx=0.5, rely=0.6, anchor="center")
        
        boton_atras.place(relx=0.49, rely=0.7, anchor="ne")
        boton_adelante.place(relx=0.51, rely=0.7, anchor="nw")

        sesion.place(relx=0.2, rely=0.2, anchor="nw")

        #se llama la funcion para estruturar la primera pagina que se muestra
        self.estructuracion_autos(self.__pagina)

        #se configura el contenedor para mostrar los autos
        for i in range(5):
            self._contenedor_autos.grid_columnconfigure(i, weight=1, pad=10)

        for i in range(2):
            self._contenedor_autos.grid_rowconfigure(i, weight=1, pad=10)

    def navegacion(self, cambio):
        #calculamos la cantidad de paginas totales con los autos que tenemos
        n_autos = len(self.__modelos)
        n_paginas = (n_autos - 1) // 5 + 1

        if cambio == None:
            cambio = 0

        #comparamos si el valor total de la pagina esta adentro del rango para hacer o no el cambio
        if self.__pagina >= 1 and self.__pagina <= n_paginas:
            self.__pagina += cambio
        else:
            print("me valio madres y no sume")


        #esto evita que el usuario acceda a una pagina diferente a las definidas 
        #limitando el rango unicamente a las que podemos crear
        if self.__pagina <= 0:
            self.__pagina = 1

        if self.__pagina >= n_paginas + 1:
            self.__pagina = n_paginas

        self.estructuracion_autos(self.__pagina)

    def estructuracion_autos(self, pagina):
        for widget in self._contenedor_autos.winfo_children():
            widget.grid_forget()

        #una vez creemos este texto hay que cambiarlo cada vez que se renueva
        #por ende creamos esta condicion
        if self.__paginacion in self.winfo_children():
            self.__paginacion.destroy()

        #calculamos las paginas totales nuevamente
        n_autos = len(self.__modelos)
        n_paginas = (n_autos - 1) // 5 + 1

        lim_inferior = 5*(pagina - 1)
        iteracion = 0

        #creamos el texto que indique en que pagina estamos
        texto_paginacion = f"{self.__pagina} / {n_paginas}"
        self.__paginacion = ctk.CTkLabel(self, text=texto_paginacion)

        self.__paginacion.place(relx=0.5, rely=0.65, anchor="center")

        for i in range(lim_inferior, lim_inferior + 5):
            if i >= len(self.autos):
                break

            #buscamos el auto correspondiente a la posicion que ocupa
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

            #se creo este boton ya que aqui se debe llevar un conteno estricto de 0 hasta la cantidad de autos
            #por lo cual esta variable va confrome a la cantidad de iteraciones y no al rango establecido
            iteracion += 1


    def menu_autos_individual(self, auto):
        for widget in self.winfo_children():
            widget.place_forget()

        #se asignan la marca, el modelo y los locales en los que se encuentra el auto
        marca = auto["marca"]
        modelo = auto["modelo"]
        lista_coincidencias = lectura_de_locales(marca, modelo)

        #se busca el diccionario que alberga los datos del auto en especifico
        datos = self.__data[marca][modelo]

        font1 = ctk.CTkFont(family="Calibri", size=24, weight="bold")

        imagen = Image.open(f"datos/convenios/{marca}/{datos["imagen"]}")

        imagen_final = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(300, 300))

        texto = f"""
        Marca: {datos["marca"]}
        Modelo: {datos["modelo"]}
        Precio: {datos["precio"]}
        Año de fabricacion: {datos["año_de_fabricacion"]}
        Caballos de fuerza: {datos["caballos_de_fuerza"]}
        Capacidad: {datos["capacidad"]}
        Peso: {datos["peso"]}
        Consumo conbinado: {datos["consumo_conbinado"]}
        Dimensiones
            Largo: {datos["dimensiones"]["largo"]}
            Ancho: {datos["dimensiones"]["ancho"]}
            Alto: {datos["dimensiones"]["alto"]}
        """
        locales_disponibles_texto = ", ".join(lista_coincidencias)
        texto_locales = "Disponible en: " + locales_disponibles_texto


        mostrar_imagen = ctk.CTkLabel(self, image=imagen_final, text="")
        datos_auto = ctk.CTkLabel(
            self, 
            text=texto,
            justify="left",
            font=font1
            )
        caracteristicas = ctk.CTkTextbox(self, width=300, height=250, activate_scrollbars=True)
        locales_disponibles = ctk.CTkTextbox(self, width=500, height=70, activate_scrollbars=True)

        simulacion = ctk.CTkButton(self, text="simulacion de cotizacion", width=200, height=70, command=lambda n = datos["precio"] :self.simular_pagos(n))
        boton_regresar = ctk.CTkButton(self, text="volver", width=100, height=50, command=self.general_mostrar_autos)

        caracteristicas.configure(state="normal")
        caracteristicas.insert("1.0", "disponible en" + datos["descripcion"])
        caracteristicas.configure(state="disabled")

        locales_disponibles.configure(state="normal")
        locales_disponibles.insert("1.0", texto_locales)
        locales_disponibles.configure(state="disabled")

        mostrar_imagen.place(relx=0.2, rely=0.2, anchor="nw")
        datos_auto.place(relx=0.4, rely=0.2, anchor="nw")
        caracteristicas.place(relx=0.2, rely=0.53, anchor="nw")
        boton_regresar.place(relx=0.7, rely=0.2, anchor="nw")
        simulacion.place(relx=0.6, rely=0.7, anchor="nw")
        locales_disponibles.place(relx=0.5, rely=0.6, anchor="nw")


    def simular_pagos(self, precio):
        #se crea la simulacion a partir de la siguiente calse
        self.__cotizacion = SimuladorFinanciamiento(master=self, precio_fijo=precio)

    def cambiar_de_sesion(self):
        #por si quieres inicia con un nuevo usuario
        self.__sesion()