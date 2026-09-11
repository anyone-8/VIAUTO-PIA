import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

# Importamos tus módulos backend
import crud_talleres
import crud_locales

RUTA_DB = "datos/libro_mayor.json"


def cargar_data():
    """Carga el JSON completo desde disco."""
    if not os.path.exists(RUTA_DB):
        os.makedirs("datos", exist_ok=True)
        data = {"talleres": {}, "locales": {}}
        with open(RUTA_DB, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return data
    with open(RUTA_DB, "r", encoding="utf-8") as f:
        return json.load(f)


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Talleres y Locales")
        self.geometry("900x600")

        # Cargamos los datos una vez y los compartimos con el backend
        self.data = cargar_data()

        self._construir_ui()
        self.refrescar_todo()

    # ------------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # ------------------------------------------------------------------
    def _construir_ui(self):
        # Pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_talleres = ttk.Frame(notebook)
        self.tab_locales = ttk.Frame(notebook)

        notebook.add(self.tab_talleres, text="Talleres")
        notebook.add(self.tab_locales, text="Locales")

        self._construir_tab_talleres()
        self._construir_tab_locales()

        # Barra de estado
        self.status = tk.StringVar(value="Listo")
        ttk.Label(self, textvariable=self.status, relief="sunken",
                  anchor="w").pack(fill="x", side="bottom")

    # -------------------------- TALLERES ------------------------------
    def _construir_tab_talleres(self):
        frame = self.tab_talleres

        # --- Formulario ---
        form = ttk.LabelFrame(frame, text="Añadir taller")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_nombre_taller = ttk.Entry(form, width=40)
        self.entry_nombre_taller.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Dirección:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_dir_taller = ttk.Entry(form, width=40)
        self.entry_dir_taller.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form, text="Añadir taller",
                   command=self.accion_añadir_taller).grid(row=0, column=2, rowspan=2, padx=10)

        # --- Tabla ---
        cols = ("clave", "id", "nombre", "direccion")
        self.tree_talleres = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree_talleres.heading(c, text=c.capitalize())
            self.tree_talleres.column(c, width=180)
        self.tree_talleres.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Botones de acción ---
        acciones = ttk.Frame(frame)
        acciones.pack(fill="x", padx=10, pady=5)

        ttk.Button(acciones, text="Eliminar seleccionado",
                   command=self.accion_eliminar_taller).pack(side="left", padx=5)
        ttk.Button(acciones, text="Refrescar",
                   command=self.refrescar_todo).pack(side="left", padx=5)

    # --------------------------- LOCALES ------------------------------
    def _construir_tab_locales(self):
        frame = self.tab_locales

        form = ttk.LabelFrame(frame, text="Añadir local")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_nombre_local = ttk.Entry(form, width=40)
        self.entry_nombre_local.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Dirección:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_dir_local = ttk.Entry(form, width=40)
        self.entry_dir_local.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form, text="Añadir local",
                   command=self.accion_añadir_local).grid(row=0, column=2, rowspan=2, padx=10)

        cols = ("clave", "id", "nombre", "direccion")
        self.tree_locales = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree_locales.heading(c, text=c.capitalize())
            self.tree_locales.column(c, width=180)
        self.tree_locales.pack(fill="both", expand=True, padx=10, pady=5)

        acciones = ttk.Frame(frame)
        acciones.pack(fill="x", padx=10, pady=5)

        ttk.Button(acciones, text="Eliminar seleccionado",
                   command=self.accion_eliminar_local).pack(side="left", padx=5)
        ttk.Button(acciones, text="Refrescar",
                   command=self.refrescar_todo).pack(side="left", padx=5)

    # ------------------------------------------------------------------
    # ACCIONES (llaman al backend)
    # ------------------------------------------------------------------
    def accion_añadir_taller(self):
        nombre = self.entry_nombre_taller.get().strip()
        direccion = self.entry_dir_taller.get().strip()

        if not nombre or not direccion:
            messagebox.showwarning("Datos incompletos",
                                   "Debes rellenar nombre y dirección.")
            return

        # Importante: recargamos data por si otro proceso la modificó
        self.data = cargar_data()
        msg = crud_talleres.añadir_taller(self.data, nombre, direccion)

        self.status.set(msg)
        self.entry_nombre_taller.delete(0, tk.END)
        self.entry_dir_taller.delete(0, tk.END)
        self.refrescar_todo()

    def accion_eliminar_taller(self):
        sel = self.tree_talleres.selection()
        if not sel:
            messagebox.showinfo("Sin selección", "Selecciona un taller.")
            return
        clave = self.tree_talleres.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar {clave}?"):
            return

        self.data = cargar_data()
        msg = crud_talleres.eliminar_taller(self.data, clave)
        self.status.set(msg)
        self.refrescar_todo()

    def accion_añadir_local(self):
        nombre = self.entry_nombre_local.get().strip()
        direccion = self.entry_dir_local.get().strip()

        if not nombre or not direccion:
            messagebox.showwarning("Datos incompletos",
                                   "Debes rellenar nombre y dirección.")
            return

        self.data = cargar_data()
        msg = crud_locales.añadir_local(self.data, nombre, direccion)

        self.status.set(msg)
        self.entry_nombre_local.delete(0, tk.END)
        self.entry_dir_local.delete(0, tk.END)
        self.refrescar_todo()

    def accion_eliminar_local(self):
        sel = self.tree_locales.selection()
        if not sel:
            messagebox.showinfo("Sin selección", "Selecciona un local.")
            return
        clave = self.tree_locales.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar {clave}?"):
            return

        self.data = cargar_data()
        msg = crud_locales.eliminar_local(self.data, clave)
        self.status.set(msg)
        self.refrescar_todo()

    # ------------------------------------------------------------------
    # REFRESCAR TABLAS
    # ------------------------------------------------------------------
    def refrescar_todo(self):
        self.data = cargar_data()

        # Talleres
        for row in self.tree_talleres.get_children():
            self.tree_talleres.delete(row)
        for clave, info in self.data.get("talleres", {}).items():
            self.tree_talleres.insert("", "end", values=(
                clave,
                info.get("id_taller", ""),
                info.get("nombre", ""),
                info.get("direccion", ""),
            ))

        # Locales
        for row in self.tree_locales.get_children():
            self.tree_locales.delete(row)
        for clave, info in self.data.get("locales", {}).items():
            self.tree_locales.insert("", "end", values=(
                clave,
                info.get("id_local", ""),
                info.get("nombre", ""),
                info.get("direccion", ""),
            ))


# ----------------------------------------------------------------------
# Alternativa: exponer funciones vía getattr() / importlib
# ----------------------------------------------------------------------
def ejecutar_accion(modulo: str, funcion: str, *args):
    """
    Ejecuta dinámicamente una función del backend.
    Ej: ejecutar_accion("crud_talleres", "añadir_taller", data, "A", "Calle 1")
    """
    import importlib
    mod = importlib.import_module(modulo)
    fn = getattr(mod, funcion)
    return fn(*args)


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
    