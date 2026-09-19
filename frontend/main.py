import tkinter as tk
from tkinter import ttk, messagebox
# sys y os nos ayudan a movernos entre las carpetas del proyecto
import sys
import os

# Esto es para que Python encuentre la carpeta 'backend' que está un nivel arriba y no marque error
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.CRUD import Libro_Mayor 

# Se crea la clase principal del programa
class AppViauto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VIAUTO-PIA - Gestion de Talleres y Locales")
        self.geometry("800x600")
        
        self.libro = Libro_Mayor()

        # Creamos las pestañas Notebook para dividir la interfaz
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Funciones que arman cada pestaña
        self.crear_pestana_talleres()
        self.crear_pestana_locales()

    #     PESTAÑA DE TALLERES 
    def crear_pestana_talleres(self):
        # Contenedor para talleres
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Talleres")

        tk.Label(frame, text="Nombre del Taller:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre_taller = tk.Entry(frame, width=30)
        self.entry_nombre_taller.grid(row=0, column=1, padx=5, pady=5)

        # Etiqueta y caja de texto para la Dirección
        tk.Label(frame, text="Dirección:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_direccion_taller = tk.Entry(frame, width=30)
        self.entry_direccion_taller.grid(row=1, column=1, padx=5, pady=5)

        # Botón para guardar el taller, llama a añadir_taller
        tk.Button(frame, text="Añadir Taller", command=self.añadir_taller).grid(row=2, column=0, columnspan=2, pady=10)
        # Botón para listar los talleres, llama a mostrar_talleres
        tk.Button(frame, text="Mostrar Talleres", command=self.mostrar_talleres).grid(row=3, column=0, columnspan=2, pady=5)

        # Lista donde se van a mostrar los tallere
        self.lista_talleres = tk.Listbox(frame, width=80, height=15)
        self.lista_talleres.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    #     PESTAÑA DE LOCALES
    def crear_pestana_locales(self):
        # Hacemos lo mismo que en talleres pero para locales
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Locales")

        tk.Label(frame, text="Nombre del Local:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre_local = tk.Entry(frame, width=30)
        self.entry_nombre_local.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Dirección:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_direccion_local = tk.Entry(frame, width=30)
        self.entry_direccion_local.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame, text="Añadir Local", command=self.añadir_local).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Mostrar Locales", command=self.mostrar_locales).grid(row=3, column=0, columnspan=2, pady=5)

        self.lista_locales = tk.Listbox(frame, width=80, height=15)
        self.lista_locales.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    #     FUNCIONES QUE CONECTAN CON EL BACKEND
    
    def añadir_taller(self):
        # Capturamos lo que el usuario escribió
        nombre = self.entry_nombre_taller.get()
        direccion = self.entry_direccion_taller.get()
        
        # Revisamos que no esten vacíos
        if nombre and direccion:
            resultado = self.libro.añadir_taller(nombre, direccion)
            messagebox.showinfo("Resultado", resultado)
            # Limpiamos las cajas para que el usuario pueda escribir otro
            self.entry_nombre_taller.delete(0, tk.END)
            self.entry_direccion_taller.delete(0, tk.END)
        else:
            # Si dejo algun lugar vacío avisamos
            messagebox.showwarning("Aviso", "Por favor llena todos los campos")

    def mostrar_talleres(self):
        self.lista_talleres.delete(0, tk.END)
        for clave, info in self.libro.data["talleres"].items():
            # Metemos cada taller a la lista visual con su clave, nombre y dirección
            self.lista_talleres.insert(tk.END, f"{clave}: {info['nombre']} - {info['direccion']}")

    def añadir_local(self):
        # Hacemos lo mismo que en añadir_taller pero con locales
        nombre = self.entry_nombre_local.get()
        direccion = self.entry_direccion_local.get()
        if nombre and direccion:
            resultado = self.libro.añadir_local(nombre, direccion)
            messagebox.showinfo("Resultado", resultado)
            self.entry_nombre_local.delete(0, tk.END)
            self.entry_direccion_local.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor llena todos los campos")

    def mostrar_locales(self):
        self.lista_locales.delete(0, tk.END)
        for clave, info in self.libro.data["locales"].items():
            self.lista_locales.insert(tk.END, f"{clave}: {info['nombre']} - {info['direccion']}")

# La ventana se abrira solo cuando corremos este archivo directamente
if __name__ == "__main__":
    app = AppViauto()
    app.mainloop()