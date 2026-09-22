#clase para el menu de abrir
import customtkinter as ctk
from backend.RI_sesiones import sesion #type: ignore

class Incio_sesion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.s = sesion()
        self.geometry("1000x500")
        self.title("Inicio de Sesion VIAUTO")

        self.bloque_nombre()
        self.bloque_contraseña()
        self.bloque_tipo()
        self.iniciar()


    def bloque_nombre(self):
        self.caja_nombre = ctk.CTkEntry(self, width=200, height=30)
        texto_nombre = ctk.CTkLabel(self, text="nombre")
        self.caja_nombre.place(relx=0.53, rely=0.3, anchor="center")
        texto_nombre.place(relx=0.4, rely=0.3, anchor="center")

    def bloque_contraseña(self):
        self.caja_contraseña = ctk.CTkEntry(self, width=200, height=30)
        texto_contraseña = ctk.CTkLabel(self, text="contraseña")
        self.caja_contraseña.place(relx=0.53, rely=0.4, anchor="center")
        texto_contraseña.place(relx=0.39, rely=0.4, anchor="center")

    def bloque_tipo(self):
        self.boton_tipo = ctk.CTkCheckBox(master=self, text="Selecciona si eres administrador")
        self.boton_tipo.place(relx=0.5, rely=0.52, anchor="center")

    def iniciar(self):
        self.boton_iniciar = ctk.CTkButton(self, text="Iniciar Sesion", command=self.comprobar)
        self.boton_iniciar.place(relx=0.5, rely=0.59, anchor="center")

    def denegado(self):
        error = ctk.CTkLabel(self, text="**Usuario o contraseña incorrecta")
        error.place(relx=0.5, rely=0.69, anchor="center")

    def comprobar(self):
        tipo = self.boton_tipo.get()
        nombre = self.caja_nombre.get()
        contraseña = self.caja_contraseña.get()

        if tipo == 1:
            tipo = "administradores"
        else:
            tipo = "usuarios"

        if self.s.verificar_datos(tipo, nombre, contraseña):
            self.acceso = tipo
            self.destroy()
        else:
            self.denegado()

    
