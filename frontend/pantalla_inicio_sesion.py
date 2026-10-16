# Clase para el menú de inicio de sesión
import customtkinter as ctk
from backend.RI_sesiones import sesion


class Inicio_sesion(ctk.CTkFrame):
    def __init__(self, master, finalizar, **kwargs):
        super().__init__(master, **kwargs)

        self.validador = finalizar
        self.login = sesion()

        self.bloque_nombre()
        self.bloque_contraseña()
        self.bloque_tipo()
        self.iniciar()

    def bloque_nombre(self):
        self.caja_nombre = ctk.CTkEntry(
            self, width=200, height=30
        )
        texto_nombre = ctk.CTkLabel(
            self, text="Nombre"
        )

        self.caja_nombre.place(
            relx=0.53, rely=0.3, anchor="center"
        )
        texto_nombre.place(
            relx=0.4, rely=0.3, anchor="center"
        )

    def bloque_contraseña(self):
        self.caja_contraseña = ctk.CTkEntry(
            self, width=200, height=30, show="*"
        )
        texto_contraseña = ctk.CTkLabel(
            self, text="Contraseña"
        )

        self.caja_contraseña.place(
            relx=0.53, rely=0.4, anchor="center"
        )
        texto_contraseña.place(
            relx=0.39, rely=0.4, anchor="center"
        )

    def bloque_tipo(self):
        self.boton_tipo = ctk.CTkCheckBox(
            master=self,
            text="Selecciona si eres administrador"
        )
        self.boton_tipo.place(
            relx=0.5, rely=0.52, anchor="center"
        )

    def iniciar(self):
        self.boton_iniciar = ctk.CTkButton(
            self,
            text="Iniciar sesión",
            command=self.comprobar
        )
        self.boton_iniciar.place(
            relx=0.5, rely=0.59, anchor="center"
        )

        self.boton_crear = ctk.CTkButton(
            self,
            text="Crear cuenta",
            command=self.crear_cuenta
        )
        self.boton_crear.place(
            relx=0.5, rely=0.68, anchor="center"
        )

    def crear_cuenta(self):
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
                "usuarios", n, c
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

    def denegado(self):
        error = ctk.CTkLabel(
            self,
            text="Usuario o contraseña incorrectos"
        )
        error.place(
            relx=0.5, rely=0.76, anchor="center"
        )

    def comprobar(self):
        tipo = self.boton_tipo.get()
        nombre = self.caja_nombre.get().strip()
        contraseña = self.caja_contraseña.get()

        if tipo == 1:
            tipo = "administradores"
        else:
            tipo = "usuarios"

        if self.login.verificar_datos(
            tipo, nombre, contraseña
        ):
            self.acceso = tipo
            self.destroy()
            self.validador()
        else:
            self.denegado()