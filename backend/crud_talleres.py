#se asume que data es el diccionario dentro de data crudo
import json
import os

def añadir_taller(data, nombre, direccion):	
	contador = 1
	while f"taller-{contador}" in data["talleres"]:
		contador += 1
	
	clave = f"taller-{contador}"
	id_taller = f"TAL-{contador}"
	
	nuevo_taller = {
        f"{clave}" : { 
            "id_taller" : f"{id_taller}",
                "nombre" : f"{nombre}",
                "direccion" : f"{direccion}",
        }
    }
	with open("datos/libro_mayor.json", "w", encoding="utf-8") as f:
		data["talleres"].update(nuevo_taller)
		json.dump(data, f, indent=4)
	
	return "se guardo con exito"
    

def eliminar_taller(data, taller):
	eliminado = data["talleres"].pop(taller, None)
			
	with open("datos/libro_mayor.json", "w", encoding="utf-8") as f:
		json.dump(data, f, indent=4)
	
	return f"se elimino lo siguiente: {eliminado}"
