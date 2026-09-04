#se asume que data es el diccionario dentro de data crudo
import json
import os


def añadir_taller(data, nombre, direccion):
	import json
	import os
	
	contador = 1
	while f"taller-0{contador}" in data["talleres"]:
		contador += 1
	
	clave = f"taller-0{contador}"
	id_taller = f"TAL-0{contador}"
	
	nuevo_taller = {
        f"{clave}" : { 
            "id_taller" : f"{id_taller}",
                "nombre" : f"{nombre}",
                "direccion" : f"{direccion}",
                "directorio" : {
                    "horarios" : "D-H-{id_taller}",
                    "servicios" : "D-S-{id_taller}",
                    "profesionales" : "D-P-{id_taller}",
                    "departamentos" : "D-D-{id_taller}",
                    "contactos" : "D-C-{id_taller}"
                }
    }
    }
	with open("datos/libro_mayor.json", "w", encoding="utf-8") as f:
		data["talleres"].update(nuevo_taller)
		json.dump(data, f, indent=4)
	
	return "se guardo con exito"
    

