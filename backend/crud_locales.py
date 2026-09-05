#se asume que data es el json completo

def añadir_local(data, nombre, direccion):
	import json
	import os
	
	contador = 1
	while f"local-0{contador}" in data["locales"]:
		contador += 1
	
	clave = f"local-0{contador}"
	id_local = f"LOC-0{contador}"
	
	nuevo_local = {
        f"{clave}" : { 
            "id_local" : f"{id_local}",
                "nombre" : f"{nombre}",
                "direccion" : f"{direccion}",
                "directorio" : {
                    "horarios" : "D-H-{id_local}",
                    "repertorio" : "D-R-{id_local}",
                    "personal" : "D-P-{id_local}",
                    "departamentos" : "D-D-{id_local}",
                    "contactos" : "D-C-{id_local}"
                }
    }
    }
	with open("datos/libro_mayor.json", "w", encoding="utf-8") as f:
		data["locales"].update(nuevo_local)
		json.dump(data, f, indent=4)
	
	return "se guardo con exito"