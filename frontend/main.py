import tkinter as tk
from tkinter import ttk, messagebox
# sys y os nos ayudan a movernos entre las carpetas del proyecto
import sys
import os

# Esto es para que Python encuentre la carpeta 'backend' que está un nivel arriba y no marque error
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos la clase Libro_Mayor del archivo CRUD.py para tener acceso a las funciones del backend
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
        tk.Button(frame, text="Mostrar Talleres", command=self.mostrar_talleres).grid(row=3, column=0, pady=5)
        # Nuevo_Botón para eliminar el taller seleccionado
        tk.Button(frame, text="Eliminar Taller", command=self.eliminar_taller).grid(row=3, column=1, pady=5)
        # Nuevo_Botón para actualizar los datos del taller seleccionado
        tk.Button(frame, text="Actualizar Datos", command=self.actualizar_taller).grid(row=4, column=0, columnspan=2, pady=5)

        # Lista donde se van a mostrar los talleres
        self.lista_talleres = tk.Listbox(frame, width=80, height=15)
        self.lista_talleres.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

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
        
        # Botones para las acciones de Mostrar, Eliminar y Actualizar para locales
        tk.Button(frame, text="Mostrar Locales", command=self.mostrar_locales).grid(row=3, column=0, pady=5)
        # Nuevo_Botón para eliminar el local seleccionado
        tk.Button(frame, text="Eliminar Local", command=self.eliminar_local).grid(row=3, column=1, pady=5)
        # Nuevo_Botón para actualizar los datos del local seleccionado
        tk.Button(frame, text="Actualizar Datos", command=self.actualizar_local).grid(row=4, column=0, columnspan=2, pady=5)

        self.lista_locales = tk.Listbox(frame, width=80, height=15)
        self.lista_locales.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

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

    def eliminar_taller(self):
        # Obtenemos cuál elemento de la lista está seleccionado
        seleccion = self.lista_talleres.curselection()
        
        # Si no hay nada seleccionado, avisamos
        if not seleccion:
            messagebox.showwarning("Aviso", "Por favor, selecciona un taller de la lista primero")
            return
        
        # Extraemos la clave (ej. "taller-1") del texto seleccionado
        item_texto = self.lista_talleres.get(seleccion[0])
        clave_taller = item_texto.split(":")[0]
        
        # Mandamos a llamar la función del backend para eliminar
        resultado = self.libro.eliminar_taller(clave_taller)
        
        # Mostramos el resultado
        if isinstance(resultado, dict):
            messagebox.showinfo("Éxito", "El taller se eliminó correctamente")
        else:
            messagebox.showinfo("Resultado", resultado)
            
        # Actualizamos la lista visual
        self.mostrar_talleres()

    def actualizar_taller(self):
        # Obtenemos el taller seleccionado de la lista
        seleccion = self.lista_talleres.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un taller de la lista primero")
            return
            
        # Obtenemos lo que el usuario escribió en las cajas de texto
        nuevo_nombre = self.entry_nombre_taller.get()
        nueva_direccion = self.entry_direccion_taller.get()
        
        # Nos aseguramos de que al menos haya escrito algo para actualizar
        if not nuevo_nombre and not nueva_direccion:
            messagebox.showwarning("Aviso", "Escribe al menos un dato nuevo (nombre o dirección) para actualizar")
            return
            
        item_texto = self.lista_talleres.get(seleccion[0])
        clave_taller = item_texto.split(":")[0]
        
        # Si escribieron un nombre nuevo, lo actualizamos
        if nuevo_nombre:
            self.libro.actualizar_taller(clave_taller, "nombre", nuevo_nombre)
            
        # Si escribieron una dirección nueva, la actualizamos
        if nueva_direccion:
            self.libro.actualizar_taller(clave_taller, "direccion", nueva_direccion)
            
        messagebox.showinfo("Éxito", "Taller actualizado correctamente")
        
        # Refrescamos la lista y limpiamos las cajas
        self.mostrar_talleres()
        self.entry_nombre_taller.delete(0, tk.END)
        self.entry_direccion_taller.delete(0, tk.END)

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

    def eliminar_local(self):
        # Obtenemos el local seleccionado
        seleccion = self.lista_locales.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Por favor, selecciona un local de la lista primero")
            return
        
        # Extraemos la clave del texto seleccionado
        item_texto = self.lista_locales.get(seleccion[0])
        clave_local = item_texto.split(":")[0]
        
        # Llamamos al backend para eliminar el local
        resultado = self.libro.eliminar_local(clave_local)
        
        if isinstance(resultado, dict):
            messagebox.showinfo("Éxito", "El local se eliminó correctamente")
        else:
            messagebox.showinfo("Resultado", resultado)
            
        # Actualizamos la lista visual
        self.mostrar_locales()

    def actualizar_local(self):
        # Obtenemos el local seleccionado
        seleccion = self.lista_locales.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un local de la lista primero")
            return
            
        # Obtenemos lo que el usuario escribió en las cajas
        nuevo_nombre = self.entry_nombre_local.get()
        nueva_direccion = self.entry_direccion_local.get()
        
        if not nuevo_nombre and not nueva_direccion:
            messagebox.showwarning("Aviso", "Escribe al menos un dato nuevo (nombre o dirección) para actualizar")
            return
            
        item_texto = self.lista_locales.get(seleccion[0])
        clave_local = item_texto.split(":")[0]
        
        # Actualizamos el nombre si es que escribieron uno nuevo
        if nuevo_nombre:
            self.libro.actualizar_local(clave_local, "nombre", nuevo_nombre)
            
        # Actualizamos la dirección si es que escribieron una nueva
        if nueva_direccion:
            self.libro.actualizar_local(clave_local, "direccion", nueva_direccion)
            
        messagebox.showinfo("Éxito", "Local actualizado correctamente")
        
        # Refrescamos la lista y limpiamos las cajas
        self.mostrar_locales()
        self.entry_nombre_local.delete(0, tk.END)
        self.entry_direccion_local.delete(0, tk.END)

# La ventana se abrira solo cuando corremos este archivo directamente
if __name__ == "__main__":
    app = AppViauto()
    app.mainloop()