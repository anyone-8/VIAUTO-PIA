#clase para añadir marcas y modelos de autos
import shutil
import os
import json
from backend.CRUD import Libro_Mayor

class Convenios:
    def __init__(self, ruta = "datos/convenios/convenios_libro_mayor.json"):
        self.json = ruta
        self.data = self.cargar_json()

        slt = Libro_Mayor()
        self.__slt = slt.data

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


    def auto_a_local(self, auto, id_local_n):
        dic_local = self.__slt["locales"][id_local_n]
        dic_auto = self.data[auto["marca"]][auto["modelo"]]
        dic_codigos = self.__slt["directorios"]["D-locales"]

        codigo_local = dic_local["id_local"]
        codigo = dic_codigos["repertorio"]
        llave = codigo.format(id_local = codigo_local)

        print(auto)
        print(id_local_n)
        print(llave)

        if not os.path.exists(f"datos/locales/{id_local_n}/{llave}/autos.json"):
            with open(f"datos/locales/{id_local_n}/{llave}/autos.json", "w", encoding="utf-8") as f:
                diccionario_puro = {
                    "autos" : {}
                }
                json.dump(diccionario_puro, f, ensure_ascii=False, indent=4)

        with open(f"datos/locales/{id_local_n}/{llave}/autos.json", "r", encoding="utf-8") as f:
            data_d_l_r = json.load(f)

        marca = dic_auto["marca"]
        modelo = dic_auto["modelo"]

        if marca not in data_d_l_r["autos"]:
            data_d_l_r["autos"][marca] = []

        if modelo not in data_d_l_r["autos"][marca]:
            data_d_l_r["autos"][marca].append(modelo)

        try:
            with open(f"datos/locales/{id_local_n}/{llave}/autos.json", "w", encoding="utf-8") as f:
                json.dump(data_d_l_r, f, indent=4)
        except:
            pass
        

        