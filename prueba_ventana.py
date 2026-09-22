#Prueba customtkinter
import customtkinter as ctk
from frontend.sesion import Incio_sesion
from frontend.main import AppViauto

#menu
menu = Incio_sesion()
menu.mainloop()

if menu.acceso == "usuarios":
    pass
else:
    admin = AppViauto()
    admin.mainloop()
