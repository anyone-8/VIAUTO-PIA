#lector de cuentas
import json

class sesion:
    def __init__(self, ruta = "datos/cuentas.json"):
        self.json = ruta
        self.data = self.cargar_json()

    def cargar_json(self):
        try:
            with open(self.json, "r", encoding="utf-8") as f:
                return json.load(f)
        #hacemos que el codigo no siga corriendo si es que no se encuentrea el json
        except(FileNotFoundError, FileExistsError, PermissionError, json.JSONDecodeError) as e:
            raise RuntimeError(f"ERROR: No se pudo leer el json: {e}")

    def guardar(self):
        try:
            with open(self.json, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            return True
    
        #Si de casualidad no se puede escribrir damos false para avisar que no se pudo}
        #relizar la accion
        except(FileExistsError, PermissionError, OSError):
            return False

    def buscar(self, tipo, nombre):
        if tipo not in ["usuarios", "administradores"]:
            return "tipo de usuario no designado en el sistema"

        for usuario, perfil in self.data[tipo].items():
            if perfil["nombre"] == nombre:
                return usuario

        return False


    def verificar_datos(self, tipo, nombre, contraseña):
        usuario = self.buscar(tipo, nombre)
        try:
            if nombre == self.data[tipo][usuario]["nombre"] and contraseña == self.data[tipo][usuario]["contraseña"]:
                return True
        except:
            return False

    def añadir_usuario(self, tipo, nombre, contraseña):
        contador = 1
        if tipo == "usuarios":
            while f"usuario-{contador}" in self.data[tipo]:
                contador += 1

            clave = f"usuario-{contador}"
            nuevo_usuario = {
                f"{clave}" : {
                    "id_usuario" : f"U-{contador}",
                    "nombre" : nombre,
                    "contraseña" : contraseña
                }
            }

            self.data[tipo].update(nuevo_usuario)
            if self.guardar():
                return "usuario añadido con exito"
            else:
                self.data[tipo].pop(clave, None)
                return "no se pudo añadir el usuario"

        if tipo == "administradores":
            while f"administrador-{contador}" in self.data[tipo]:
                contador += 1
        
            clave = f"administrador-{contador}"
            nuevo_administrador = {
                f"{clave}" : {
                    "id_administrador" : f"A-{contador}",
                    "nombre" : nombre,
                    "contraseña" : contraseña
                }
            }
        
            self.data[tipo].update(nuevo_administrador)
            if self.guardar():
                return "administrador añadido con exito"
            else:
                self.data[tipo].pop(clave, None)
                return "no se pudo añadir el usuario"

            

        