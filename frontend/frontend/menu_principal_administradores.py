#clase para cerar el menu pricipal
from backend.CRUD_convenios import Convenios
from frontend.gui_autos_v2 import Menu_gui_autos
from frontend.menu_marcas import menu_marcas
from frontend.añadir_auto_a_local import Menu_Sutir_Local
from frontend.menu_añdir_lt import Menu_Añadir_local_taller
from backend.RI_sesiones import sesion
import customtkinter as ctk

class principal_administradores(ctk.CTkFrame):
    def __init__(self, master, inicio_sesion, **kwargs):
        super().__init__(master, **kwargs)

        self.convenios = Convenios()
        self.login = sesion()
        self.__sesion = inicio_sesion
        self.opciones()

    def opciones(self):
        self.__opciones = {}

        self.__opciones["place"] = {}

        e_place = self.__opciones["place"]

        e_place["boton_autos"] = ctk.CTkButton(self, text="Catalogo de autos", width=150, height=100, command=self.menu_autos)
        e_place["boton_añadir_marca"] = ctk.CTkButton(self, text="añadir marca\n a convenios", width=150, height=100, command=self.menu_añadir_marca)
        e_place["boton_añadir_a_local"] = ctk.CTkButton(self, text="añadir auto\n a local", width=150, height=100, command=self.añadir_carro_local)
        e_place["boton_sesion"] = ctk.CTkButton(self, text="cambiar de sesion", width=100, height=40, command=self.cambiar_de_sesion)
        e_place["boton_añadir_local_taller"] = ctk.CTkButton(self, text="añadir\n local y taller", width=150, height=100, command=self.añadir_local_taller)
        e_place["boton_admin"] = ctk.CTkButton(self, text="añadir\n administrador", width=150, height=100, command=self.añadir_administrador)
        

        e_place["boton_autos"].place(relx=0.20, rely=0.40, anchor="nw")
        e_place["boton_añadir_marca"].place(relx=0.4, rely=0.4, anchor="nw")
        e_place["boton_añadir_a_local"].place(relx=0.65, rely=0.4, anchor="nw")
        e_place["boton_añadir_local_taller"].place(relx=0.3, rely=0.6, anchor="nw")
        e_place["boton_admin"].place(relx=0.6, rely=0.6, anchor="nw")
        e_place["boton_sesion"].place(relx=0.2, rely=0.2, anchor="center")


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

    def añadir_local_taller(self):
        self.gui_menu_local_taller = Menu_Añadir_local_taller(master=self)

    def añadir_administrador(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Crear cuenta")
        ventana.geometry("350x270")
        ventana.resizable(False, False)

        nombre = ctk.CTkEntry(
            ventana,
            placeholder_text="Nombre de usuario",
            width=220
        )
        nombre.pack(pady=(20, 10))

        contraseña = ctk.CTkEntry(
            ventana,
            placeholder_text="Contraseña",
            show="*",
            width=220
        )
        contraseña.pack(pady=10)

        mensaje = ctk.CTkLabel(
            ventana, text=""
        )
        mensaje.pack(pady=5)

        def registrar():
            n = nombre.get().strip()
            c = contraseña.get().strip()

            if not n or not c:
                mensaje.configure(
                    text="Completa ambos campos"
                )
                return

            resultado = self.login.añadir_usuario(
                "administradores", n, c
            )

            mensaje.configure(text=resultado)

            if resultado == "usuario añadido con exito":
                nombre.configure(state="disabled")
                contraseña.configure(state="disabled")
                boton_registrar.configure(state="disabled")

        boton_registrar = ctk.CTkButton(
            ventana,
            text="Registrarme",
            command=registrar
        )
        boton_registrar.pack(pady=10)


    def ocultar_opciones(self):
        for widget in self.__opciones["place"].values():
            widget.place_forget()

    def cambiar_de_sesion(self):
        #por si quieres inicia con un nuevo usuario
        self.__sesion()

    

    