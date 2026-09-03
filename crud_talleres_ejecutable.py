from crud_talleres import añadir_taller_back
import os
import json

with open("datos/libro_mayor.json", "r", encoding="utf-8") as f:
    data = json.load(f)

#supongamos que nos dan el data crudo
def añadir_taller(data):
    nuevo_taller = añadir_taller_back(data["talleres"])

    with open("datos/libro_mayor.json", "w", encoding="utf-8") as f:
        data["talleres"].update(nuevo_taller)
        json.dump(data, f, indent=4)

    print("taller guardado con exito")

añadir_taller(data)