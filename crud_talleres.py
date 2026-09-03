#se asume que data es el diccionario dentro de data["talleres"]

def añadir_taller_back(data):
    direccion = input("indique la direccion (municipio, estado): ")
    nombre = input("indique el nombre de la sucursal")

    contador = 1
    while f"taller-0{contador}" in data:
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
    return nuevo_taller
    

