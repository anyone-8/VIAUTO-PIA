#creamos una clase para calar su funcionamiento
import json
import os

class Libro_Mayor:
    #el corazon self es quien contiene todo nuestro diccionario
    def __init__(self, ruta = "datos/libro_mayor.json"):
        self.json = ruta
        self.data = self.cargar_json()

    #funcion que carga json a memoria local
    def cargar_json(self):
        with open(self.json, "r", encoding="utf-8") as f:
            return json.load(f)

    #funcion que guarda las acciones que se realicen en el json
    def guardar(self):
        with open(self.json, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    #supongo que los nombres ya son descriptivos
    def añadir_taller(self, nombre, direccion):
        #nos aseguramos que creemos siempre un taller o en un espacio vacio
        #o en el siguiente disponible n + 1 siendo n el ultimo taller
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
        self.data["talleres"][clave] = nuevo_taller
        self.guardar()
        return "se guardo con exito"

    def eliminar_taller(self, taller):
        #se elimina el taller y se guarda
        eliminado = self.data["talleres"].pop(taller, None)
        self.guardar()
        #se devuelve el dato eliminado
        return eliminado

    def actualizar_taller(self, taller, editar, elemento):
        #en base al taller, lo que se quiere editar (nombre o direccion) y la nueva
        #infromacion se actualiza dicho dato en memoria y se guarda en el json
        self.data["talleres"][taller][editar] = elemento
        self.guardar()
        return f"se actualizo {editar} con exito"

    def mostrar_taller(self, taller):
        #se devuelve un pequeño diccionario en base a nombre y taller
        info = {"nombre" : f"{self.data["talleres"][taller]["nombre"]}",
                "direccion" : f"{self.data["talleres"][taller]["direccion"]}"}

        return info

    def añadir_local(self, nombre, direccion):
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
        self.data["locales"][clave] = nuevo_local
        self.guardar()
        return "se guardo con exito"

    def eliminar_local(self, local):
        #se elimina el local de la memoria, se actualiza el json y se devuelve
        #el local eliminado
        eliminado = self.data["locales"].pop(local, None)
        self.guardar()
        return eliminado


    def actualizar_local(self, local, editar, elemento):
        #se actualiza en base al local, lo que se quiere editar (nombre o local)
        #y lo que va a sustituir la informacion y se guarda
        self.data["locales"][local][editar] = elemento
        self.guardar()
        return f"se actualizo {editar} con exito"
    

    def mostrar_local(self, local):
        #en base el taller devuelve su nombre y direccion
        info = {"nombre" : f"{self.data["locales"][local]["nombre"]}",
                "direccion" : f"{self.data["locales"][local]["direccion"]}"}
        
        return info