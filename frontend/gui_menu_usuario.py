import json
import customtkinter as ctk
from pathlib import Path
from PIL import Image
from tkinter import messagebox


class Menu_Usuario(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.ruta_json = (
            Path(__file__).resolve().parents[1]
            / "datos"
            / "convenios"
            / "convenios_libro_mayor.json"
        )

        self.ruta_imagenes = (
            Path(__file__).resolve().parents[1]
            / "datos"
            / "convenios"
        )

        self.autos = []
        self.indice = 0
        self.imagen_actual = None

        self.cargar_autos()
        self.crear_interfaz()

    def cargar_autos(self):
        try:
            with open(self.ruta_json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            for marca, modelos in datos.items():
                for clave, informacion in modelos.items():
                    auto = informacion.copy()
                    auto.setdefault("marca", marca)
                    auto.setdefault("modelo", clave)
                    self.autos.append(auto)

        except (OSError, json.JSONDecodeError) as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los autos:\n{error}"
            )

    def crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        titulo = ctk.CTkLabel(
            self,
            text="Autos disponibles",
            font=ctk.CTkFont(family="Calibri", size=28, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=20)

        self.tarjeta = ctk.CTkFrame(self, width=650, height=450)
        self.tarjeta.grid(row=1, column=0, padx=20, pady=10)
        self.tarjeta.grid_columnconfigure(0, weight=1)

        self.etiqueta_imagen = ctk.CTkLabel(
            self.tarjeta,
            text="",
            width=400,
            height=220
        )
        self.etiqueta_imagen.grid(row=0, column=0, pady=10)

        self.etiqueta_nombre = ctk.CTkLabel(
            self.tarjeta,
            text="",
            font=ctk.CTkFont(size=23, weight="bold")
        )
        self.etiqueta_nombre.grid(row=1, column=0, pady=5)

        self.etiqueta_marca = ctk.CTkLabel(
            self.tarjeta,
            text="",
            font=ctk.CTkFont(size=17)
        )
        self.etiqueta_marca.grid(row=2, column=0, pady=5)

        self.etiqueta_precio = ctk.CTkLabel(
            self.tarjeta,
            text="",
            font=ctk.CTkFont(size=19, weight="bold")
        )
        self.etiqueta_precio.grid(row=3, column=0, pady=5)

        navegacion = ctk.CTkFrame(self, fg_color="transparent")
        navegacion.grid(row=2, column=0, pady=15)

        ctk.CTkButton(
            navegacion,
            text="← Anterior",
            command=lambda: self.navegar(-1)
        ).pack(side="left", padx=10)

        self.etiqueta_pagina = ctk.CTkLabel(
            navegacion,
            text=""
        )
        self.etiqueta_pagina.pack(side="left", padx=10)

        ctk.CTkButton(
            navegacion,
            text="Siguiente →",
            command=lambda: self.navegar(1)
        ).pack(side="left", padx=10)

        self.mostrar_auto()

    def mostrar_auto(self):
        if not self.autos:
            self.etiqueta_nombre.configure(text="No hay autos disponibles")
            self.etiqueta_marca.configure(text="")
            self.etiqueta_precio.configure(text="")
            self.etiqueta_imagen.configure(
                image=None,
                text="No hay autos registrados"
            )
            self.etiqueta_pagina.configure(text="0 / 0")
            return

        auto = self.autos[self.indice]

        self.etiqueta_nombre.configure(
            text=auto.get("modelo", "Modelo no disponible")
        )

        self.etiqueta_marca.configure(
            text=f"Marca: {auto.get('marca', 'No disponible')}"
        )

        precio = auto.get("precio")
        if isinstance(precio, (int, float)):
            texto_precio = f"Precio: ${precio:,.2f} MXN"
        else:
            texto_precio = "Precio no disponible"

        self.etiqueta_precio.configure(text=texto_precio)
        self.etiqueta_pagina.configure(
            text=f"{self.indice + 1} / {len(self.autos)}"
        )

        ruta = self.ruta_imagenes / auto.get("imagen", "")

        try:
            if not ruta.is_file():
                raise FileNotFoundError(str(ruta))

            imagen_pil = Image.open(ruta)
            self.imagen_actual = ctk.CTkImage(
                light_image=imagen_pil,
                dark_image=imagen_pil,
                size=(400, 220)
            )

            self.etiqueta_imagen.configure(
                image=self.imagen_actual,
                text=""
            )

        except (OSError, ValueError):
            self.imagen_actual = None
            self.etiqueta_imagen.configure(
                image=None,
                text="Imagen no disponible"
            )

    def navegar(self, cambio):
        if not self.autos:
            return

        self.indice = (self.indice + cambio) % len(self.autos)
        self.mostrar_auto()