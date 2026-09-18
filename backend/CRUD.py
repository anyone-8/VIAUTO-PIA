#creamos una clase para calar su funcionamiento
import json
from .carpetas import crear_carpetas, borrar_carpetas

class Libro_Mayor:
    #el corazon self es quien contiene todo nuestro diccionario
    def __init__(self, ruta = "datos/libro_mayor.json"):
        self.json = ruta
        self.data = self.cargar_json()

    #funcion que carga json a memoria local
    def cargar_json(self):
        try:
            with open(self.json, "r", encoding="utf-8") as f:
                return json.load(f)
        #hacemos que el codigo no siga corriendo si es que no se encuentrea el json
        except(FileNotFoundError, FileExistsError, PermissionError, json.JSONDecodeError) as e:
            raise RuntimeError(f"ERROR: No se pudo leer el json: {e}")

    #funcion que guarda las acciones que se realicen en el json
    def guardar(self):
        try:
            with open(self.json, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            return True

        #Si de casualidad no se puede escribrir damos false para avisar que no se pudo}
        #relizar la accion
        except(FileExistsError, PermissionError, OSError):
            return False

    #supongo que los nombres ya son descriptivos
    def añadir_taller(self, nombre, direccion):
        #nos aseguramos que creemos siempre un taller o en un espacio vacio
        #o en el siguiente disponible n + 1 siendo n el ultimo taller
        funcion = "talleres"
        contador = 1
        while f"taller-{contador}" in self.data["talleres"]:
            contador += 1

        #se crea el nuevo taller    
        clave = f"taller-{contador}"
        id_taller = f"TAL-{contador}"
            
        nuevo_taller = {
            f"{clave}" : { 
                "id_taller" : f"{id_taller}",
                    "nombre" : f"{nombre}",
                    "direccion" : f"{direccion}",
            }
        }

        #se guarda en el json y, ademas, se devulve que se completo con exito
        self.data["talleres"].update(nuevo_taller)
        if self.guardar():
            crear_carpetas(self.data, funcion, clave, id_taller)
            return "se guardo con exito"
        else:
            self.data["talleres"].pop(clave, None)
            return "no se pudo guardar el taller"

    def eliminar_taller(self, taller):
        funcion = "talleres"
        if taller not in self.data["talleres"]:
            return "El taller no existe"

        #se elimina el taller y se guarda
        eliminado = self.data["talleres"].pop(taller, None)
        #comprobamos si se puede guardar el archivo
        if self.guardar():
            #se devuelve el dato eliminado
            borrar_carpetas(self.data, funcion, taller)
            return eliminado
        #en caso no se pueda eliminar
        else:
            self.data["talleres"][taller] = eliminado
            return "no se pudo eliminar el archivo"
        
        

    def actualizar_taller(self, taller, editar, elemento):
        #manejamos errores de llenado
        if taller not in self.data["talleres"]:
            return "el taller no existe"
        elif editar not in self.data["talleres"][taller]:
            return "el taller no existe"
        #en base al taller, lo que se quiere editar (nombre o direccion) y la nueva
        #infromacion se actualiza dicho dato en memoria y se guarda en el json
        respaldo = self.data["talleres"][taller][editar]
        self.data["talleres"][taller][editar] = elemento

        if self.guardar():
            return f"se actualizo {editar} con exito"
        else:
            self.data["talleres"][taller][editar] = respaldo
            return "no se puede guardar"
            

    def mostrar_taller(self, taller):
        if taller not in self.data["talleres"]:
            return "el taller no existe"
        #se devuelve un pequeño diccionario en base a nombre y taller
        info = {"nombre" : f"{self.data["talleres"][taller]["nombre"]}",
                "direccion" : f"{self.data["talleres"][taller]["direccion"]}"}

        return info

    def añadir_local(self, nombre, direccion):
        funcion = "locales"
        #corrobora en usar el primer local desocupado o el n+1
        contador = 1
        while f"local-{contador}" in self.data["locales"]:
            contador += 1

        #crea el nuevo local
        clave = f"local-{contador}"
        id_local = f"LOC-{contador}"
            
        nuevo_local = {
            f"{clave}" : { 
                "id_local" : f"{id_local}",
                "nombre" : f"{nombre}",
                "direccion" : f"{direccion}",
                }
        }

        #añade el local al json y lo guarda
        self.data["locales"].update(nuevo_local)
        if self.guardar():
            crear_carpetas(self.data, funcion, clave, id_local)
            return "se guardo con exito"
        else:
            self.data["locales"].pop(clave, None)
            return "no se pudo guardar el archivo"

    def eliminar_local(self, local):
        funcion = "locales"
        #se elimina el local de la memoria, se actualiza el json y se devuelve
        #el local eliminado
        if local not in self.data["locales"]:
            return "no existe le local"
        
        eliminado = self.data["locales"].pop(local, None)
        if self.guardar():
            borrar_carpetas(self.data, funcion, local)
            return eliminado
        else:
            self.data["locales"][local] = eliminado
            return "no se pudo guardar el archivo"


    def actualizar_local(self, local, editar, elemento):
        if local not in self.data["locales"]:
            return "el local no exite"
        elif editar not in self.data["locales"][local]:
            return "no existe el elemento a modificar"
        #se actualiza en base al local, lo que se quiere editar (nombre o local)
        #y lo que va a sustituir la informacion y se guarda
        respaldo = self.data["locales"][local][editar]
        self.data["locales"][local][editar] = elemento

        if self.guardar():
            return f"se actualizo {editar} con exito"
        else:
            self.data["locales"][local][editar] = respaldo
            return "no se pudo guardar"
    

    def mostrar_local(self, local):
        if local not in self.data["locales"]:
            return "el local no existe"
        #en base el taller devuelve su nombre y direccion
        info = {"nombre" : f"{self.data["locales"][local]["nombre"]}",
                "direccion" : f"{self.data["locales"][local]["direccion"]}"}
        
        return info
