#se asume que data es el json completo
import json
import os

#funcion para añadir un local
def añadir_local(data, nombre, direccion):
	contador = 1
	while f"local-{contador}" in data["locales"]:
		contador += 1
	
	clave = f"local-{contador}"
	id_local = f"LOC-{contador}"
	
	nuevo_local = {
        f"{clave}" : { 
            "id_local" : f"{id_local}",
            "nombre" : f"{nombre}",
            "direccion" : f"{direccion}",
			}
    }
    
	with open("datos/libro_mayor.json", "w", encoding="utf-8") as f:
		data["locales"].update(nuevo_local)
		json.dump(data, f, indent=4)
	
	return "se guardo con exito"

#suponemos que nos dan numero de sucursal
def eliminar_local(data, local):
	eliminado = data["locales"].pop(local, None)
			
	with open("datos/libro_mayor.json", "w", encoding="utf-8") as f:
		json.dump(data, f, indent=4)
	
	return f"se elimino lo siguiente: {eliminado}"

