import os
from pathlib import Path
import shutil
#supongamos que
#self es self.data de nuestra clase, funcion es si es taller o local
#clave es la clave generada, identificador el identificador generado

def crear_carpetas(data, funcion, clave, identificador):
    if funcion == "talleres":
        formato = {"id_taller" : identificador}
    elif funcion == "locales":
        formato = {"id_local" : identificador}
    else:
        raise ValueError(f"hay un error con: {funcion}")

    
    for directorios in data["directorios"][f"D-{funcion}"].values():
        codigo = directorios.format(**formato)
        ruta = os.path.join("datos", funcion, clave, codigo)
        os.makedirs(ruta, exist_ok=True)

def borrar_carpetas(data, funcion, clave):
    ruta = Path(f"datos/{funcion}/{clave}")
    if ruta.exists() and ruta.is_dir():
        shutil.rmtree(ruta)