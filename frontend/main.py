import customtkinter as ctk
from tkinter import messagebox
# sys y os nos ayudan a movernos entre las carpetas del proyecto
import sys
import os

# Esto es para que Python encuentre la carpeta 'backend' que está un nivel arriba y no marque error
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos la clase Libro_Mayor del archivo CRUD.py
from backend.CRUD import Libro_Mayor

# Se crea la clase principal del programa
class AppViauto(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VIAUTO-PIA - Gestion de Talleres y Locales")
        self.geometry("800x600")

        self.libro = Libro_Mayor()

        # Variables para guardar el taller o local seleccionado
        self.taller_seleccionado = None
        self.local_seleccionado = None

        # Creamos las pestañas para dividir la interfaz
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Funciones que arman cada pestaña
        self.crear_pestana_talleres()
        self.crear_pestana_locales()

    #     PESTAÑA DE TALLERES
    def crear_pestana_talleres(self):
        # Contenedor para talleres
        frame = self.notebook.add("Talleres")

        ctk.CTkLabel(frame, text="Nombre del Taller:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.entry_nombre_taller = ctk.CTkEntry(frame, width=250)
        self.entry_nombre_taller.grid(
            row=0, column=1, padx=5, pady=5
        )

        # Etiqueta y caja de texto para la Dirección
        ctk.CTkLabel(frame, text="Dirección:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.entry_direccion_taller = ctk.CTkEntry(frame, width=250)
        self.entry_direccion_taller.grid(
            row=1, column=1, padx=5, pady=5
        )

        # Botón para guardar el taller, llama a añadir_taller
        ctk.CTkButton(
            frame,
            text="Añadir Taller",
            command=self.añadir_taller
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Botones para mostrar, eliminar y actualizar talleres
        ctk.CTkButton(
            frame,
            text="Mostrar Talleres",
            command=self.mostrar_talleres
        ).grid(row=3, column=0, pady=5)

        ctk.CTkButton(
            frame,
            text="Eliminar Taller",
            command=self.eliminar_taller
        ).grid(row=3, column=1, pady=5)

        ctk.CTkButton(
            frame,
            text="Actualizar Datos",
            command=self.actualizar_taller
        ).grid(row=4, column=0, columnspan=2, pady=5)

        # Lista desplazable donde se mostrarán y seleccionarán los talleres
        self.lista_talleres = ctk.CTkScrollableFrame(
            frame,
            width=650,
            height=230,
            label_text="Lista de talleres"
        )
        self.lista_talleres.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10
        )

    #     PESTAÑA DE LOCALES
    def crear_pestana_locales(self):
        # Hacemos lo mismo que en talleres pero para locales
        frame = self.notebook.add("Locales")

        ctk.CTkLabel(frame, text="Nombre del Local:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.entry_nombre_local = ctk.CTkEntry(frame, width=250)
        self.entry_nombre_local.grid(
            row=0, column=1, padx=5, pady=5
        )

        ctk.CTkLabel(frame, text="Dirección:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.entry_direccion_local = ctk.CTkEntry(frame, width=250)
        self.entry_direccion_local.grid(
            row=1, column=1, padx=5, pady=5
        )

        ctk.CTkButton(
            frame,
            text="Añadir Local",
            command=self.añadir_local
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Botones para las acciones de Mostrar, Eliminar y Actualizar para locales
        ctk.CTkButton(
            frame,
            text="Mostrar Locales",
            command=self.mostrar_locales
        ).grid(row=3, column=0, pady=5)

        ctk.CTkButton(
            frame,
            text="Eliminar Local",
            command=self.eliminar_local
        ).grid(row=3, column=1, pady=5)

        ctk.CTkButton(
            frame,
            text="Actualizar Datos",
            command=self.actualizar_local
        ).grid(row=4, column=0, columnspan=2, pady=5)

        # Lista desplazable donde se mostrarán y seleccionarán los locales
        self.lista_locales = ctk.CTkScrollableFrame(
            frame,
            width=650,
            height=230,
            label_text="Lista de locales"
        )
        self.lista_locales.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10
        )

    #     FUNCIONES QUE CONECTAN CON EL BACKEND

    # Función para mostrar los talleres y permitir seleccionarlos
    def mostrar_talleres(self):
        # Eliminamos los botones anteriores de la lista
        for widget in self.lista_talleres.winfo_children():
            widget.destroy()

        # Reiniciamos la selección
        self.taller_seleccionado = None

        # Mostramos los talleres disponibles
        for clave, info in self.libro.data["talleres"].items():
            fila = ctk.CTkButton(
                self.lista_talleres,
                text=f"{clave}: {info['nombre']} - {info['direccion']}",
                anchor="w",
                fg_color="transparent",
                text_color=("black", "white"),
                hover_color=("gray85", "gray25"),
                command=lambda c=clave: self.seleccionar_taller(c)
            )
            fila.pack(fill="x", padx=5, pady=3)

    # Función para seleccionar y resaltar un taller
    def seleccionar_taller(self, clave):
        self.taller_seleccionado = clave

        # Resaltamos el taller seleccionado
        for widget in self.lista_talleres.winfo_children():
            widget.configure(fg_color="transparent")

        for widget in self.lista_talleres.winfo_children():
            if widget.cget("text").startswith(clave + ":"):
                widget.configure(fg_color=("#B8A1E3", "#59447D"))

    # Igual para locales
    def mostrar_locales(self):
        for widget in self.lista_locales.winfo_children():
            widget.destroy()

        self.local_seleccionado = None

        for clave, info in self.libro.data["locales"].items():
            fila = ctk.CTkButton(
                self.lista_locales,
                text=f"{clave}: {info['nombre']} - {info['direccion']}",
                anchor="w",
                fg_color="transparent",
                text_color=("black", "white"),
                hover_color=("gray85", "gray25"),
                command=lambda c=clave: self.seleccionar_local(c)
            )
            fila.pack(fill="x", padx=5, pady=3)

    def seleccionar_local(self, clave):
        self.local_seleccionado = clave

        for widget in self.lista_locales.winfo_children():
            widget.configure(fg_color="transparent")

        for widget in self.lista_locales.winfo_children():
            if widget.cget("text").startswith(clave + ":"):
                widget.configure(fg_color=("#B8A1E3", "#59447D"))

    def añadir_taller(self):
        # Capturamos lo que el usuario escribió
        nombre = self.entry_nombre_taller.get()
        direccion = self.entry_direccion_taller.get()

        # Revisamos que no estén vacíos
        if nombre and direccion:
            resultado = self.libro.añadir_taller(nombre, direccion)
            messagebox.showinfo("Resultado", resultado)

            self.entry_nombre_taller.delete(0, "end")
            self.entry_direccion_taller.delete(0, "end")

            # Actualizamos la lista visual
            self.mostrar_talleres()
        else:
            # Si dejó algún lugar vacío avisamos
            messagebox.showwarning(
                "Aviso",
                "Por favor llena todos los campos"
            )

    def eliminar_taller(self):
        # Obtenemos la clave del taller seleccionado
        clave_taller = self.taller_seleccionado

        # Si no hay nada seleccionado, avisamos
        if not clave_taller:
            messagebox.showwarning(
                "Aviso",
                "Por favor, selecciona un taller de la lista primero"
            )
            return

        # Mandamos a llamar la función del backend para eliminar
        resultado = self.libro.eliminar_taller(clave_taller)

        # Mostramos el resultado
        if isinstance(resultado, dict):
            messagebox.showinfo(
                "Éxito",
                "El taller se eliminó correctamente"
            )
        else:
            messagebox.showinfo("Resultado", resultado)

        # Actualizamos la lista visual
        self.mostrar_talleres()

    def actualizar_taller(self):
        # Obtenemos el taller seleccionado de la lista
        clave_taller = self.taller_seleccionado

        if not clave_taller:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un taller de la lista primero"
            )
            return

        # Obtenemos lo que el usuario escribió en las cajas de texto
        nuevo_nombre = self.entry_nombre_taller.get()
        nueva_direccion = self.entry_direccion_taller.get()

        # Nos aseguramos de que al menos haya escrito algo para actualizar
        if not nuevo_nombre and not nueva_direccion:
            messagebox.showwarning(
                "Aviso",
                "Escribe al menos un dato nuevo (nombre o dirección) para actualizar"
            )
            return

        # Si escribieron un nombre nuevo, lo actualizamos
        if nuevo_nombre:
            self.libro.actualizar_taller(
                clave_taller, "nombre", nuevo_nombre
            )

        # Si escribieron una dirección nueva, la actualizamos
        if nueva_direccion:
            self.libro.actualizar_taller(
                clave_taller, "direccion", nueva_direccion
            )

        messagebox.showinfo(
            "Éxito",
            "Taller actualizado correctamente"
        )

        # Refrescamos la lista y limpiamos las cajas
        self.mostrar_talleres()
        self.entry_nombre_taller.delete(0, "end")
        self.entry_direccion_taller.delete(0, "end")

    def añadir_local(self):
        # Hacemos lo mismo que en añadir_taller pero con locales
        nombre = self.entry_nombre_local.get()
        direccion = self.entry_direccion_local.get()

        if nombre and direccion:
            resultado = self.libro.añadir_local(nombre, direccion)
            messagebox.showinfo("Resultado", resultado)

            self.entry_nombre_local.delete(0, "end")
            self.entry_direccion_local.delete(0, "end")

            # Actualizamos la lista visual
            self.mostrar_locales()
        else:
            messagebox.showwarning(
                "Aviso",
                "Por favor llena todos los campos"
            )

    def eliminar_local(self):
        clave_local = self.local_seleccionado

        if not clave_local:
            messagebox.showwarning(
                "Aviso",
                "Por favor, selecciona un local de la lista primero"
            )
            return

        resultado = self.libro.eliminar_local(clave_local)

        if isinstance(resultado, dict):
            messagebox.showinfo(
                "Éxito",
                "El local se eliminó correctamente"
            )
        else:
            messagebox.showinfo("Resultado", resultado)

        # Actualizamos la lista visual
        self.mostrar_locales()

    def actualizar_local(self):
        clave_local = self.local_seleccionado

        if not clave_local:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un local de la lista primero"
            )
            return

        nuevo_nombre = self.entry_nombre_local.get()
        nueva_direccion = self.entry_direccion_local.get()

        if not nuevo_nombre and not nueva_direccion:
            messagebox.showwarning(
                "Aviso",
                "Escribe al menos un dato nuevo (nombre o dirección) para actualizar"
            )
            return

        if nuevo_nombre:
            self.libro.actualizar_local(
                clave_local, "nombre", nuevo_nombre
            )


        if nueva_direccion:
            self.libro.actualizar_local(
                clave_local, "direccion", nueva_direccion
            )

        messagebox.showinfo(
            "Éxito",
            "Local actualizado correctamente"
        )

        # Refrescamos la lista y limpiamos las cajas
        self.mostrar_locales()
        self.entry_nombre_local.delete(0, "end")
        self.entry_direccion_local.delete(0, "end")


# La ventana se abrirá solo cuando corremos este archivo directamente
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = AppViauto()
    app.mainloop()