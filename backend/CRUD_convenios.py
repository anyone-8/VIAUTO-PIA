#clase para añadir marcas y modelos de autos
import shutil
import os
import json

class Convenios:
    def __init__(self, ruta = "datos/convenios/convenios_libro_mayor.json"):
        self.json = ruta
        self.data = self.cargar_json()

    def cargar_json(self):
        try:
            with open(self.json, "r", encoding="utf-8") as f:
                return json.load(f)
        #hacemos que el codigo no siga corriendo si es que no se encuentrea el json, no funciona, correjir
        except(FileNotFoundError, FileExistsError, PermissionError, json.JSONDecodeError) as e:
            raise RuntimeError(f"ERROR: No se pudo leer el json: {e}")

    def guardar_json(self):
        try:
            with open(self.json, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
                return True
        
        #Si de casualidad no se puede escribrir damos false para avisar que no se pudo}
        #relizar la accion
        except(FileExistsError, PermissionError, OSError):
            return False

    def añadir_marca(self, marca):
        #verificamos si la marca ya existe
        if marca in self.data:
            return "marca ya existente"

        #añadimos nueva marca
        self.data.update({f"{marca}": {}})
        if self.guardar_json():
            carpeta = os.path.join(f"datos/convenios/{marca}")
            os.makedirs(carpeta, exist_ok=True)


            return f"se guardo la marca {marca} con exito"
        else:
            self.data.pop(marca, None)
            return "No se pudo guardar la marca"

    #en base a un diccionario con todos los elementos se realiza el llenado de un nuevo modelo de auto
    def añadir_modelo(self, formulario, imagen):
        for modelo in self.data[formulario["marca"]].keys():
            if modelo.lower().replace("_", "") == formulario["modelo"].lower().replace(" ", "").replace("_", ""):
                return False

        self.data[formulario["marca"]].update({formulario["modelo"] : formulario})

        if self.guardar_json():

            print(imagen)
            nombre_base_imagen = os.path.basename(imagen)
            print(nombre_base_imagen)
            nombre_puente = os.path.join(f"datos/convenios/{formulario["marca"]}/{nombre_base_imagen}")
            print(nombre_puente)
            shutil.copy2(imagen, nombre_puente)
            os.rename(nombre_puente, f"datos/convenios/{formulario["marca"]}/{formulario["imagen"]}")

        else:
            return False

        

        