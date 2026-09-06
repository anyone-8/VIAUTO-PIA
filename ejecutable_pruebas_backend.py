#ejecutable de prubas
import os
import json
from backend.crud_talleres import añadir_taller

with open("datos/libro_mayor.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
"""
nombre = input("introduzca el nombre del nuevo taller: ")

direccion = input("indique la direccion del taller (municipio, estado): ")

print(añadir_taller(data, nombre, direccion))
"""

nombre = input("indique el nombre del nuevo local: ")

direccion = input("indique la direccion del local (municipio, estado): ") 

print(añadir_local(data, nombre, direccion))
