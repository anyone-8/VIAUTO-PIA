#lector de todos los autos de los locales
from .CRUD import Libro_Mayor
import os
import json

def lectura_de_locales(marca, modelo):
    libro = Libro_Mayor()
    datos_locales = libro.data["locales"]
    direc = libro.data["directorios"]["D-locales"]["repertorio"]

    num_local = [local for local in datos_locales.keys()]
    codigos = [identificador["id_local"] for identificador in datos_locales.values()]
    accesos = []
    locales_con_auto = []

    for i in range(len(codigos)):
        llave = direc.format(id_local=codigos[i])
        accesos.append(llave)

    for i in range(len(accesos)):
        with open(f"datos/locales/{num_local[i]}/{accesos[i]}/autos.json", "r", encoding="utf-8") as f:
            dato = json.load(f)

            if marca in dato["autos"] and modelo in dato["autos"][marca]:
                locales_con_auto.append(datos_locales[num_local[i]]["nombre"])

    return locales_con_auto

                


    