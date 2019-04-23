
class ErrorIngreso(Exception):
    def __init__(self, tipo):
        # Sobreescribimos el __init__ para cambiar el ingreso de los parámetros
        texto = ""
        if tipo == "usuario":
            texto = "El usuario ingresado no fue encontrado."
        elif tipo == "contraseña":
            texto = "La contraseña no coincide con el usuario."
        elif tipo == "usuario_rep":
            texto = "Este usuario ya inició sesión"
        super().__init__(texto)

class ErrorRegistro(Exception):
    def __init__(self, tipo):
        texto = ""
        if tipo == "usuario":
            texto = "El usuario tiene dígitos que no soportamos."
        elif tipo == "usuario_rep":
            texto = "Este usuario ya existe."
        elif tipo == "contraseña":
            texto = "Las contraseñas no coinciden."
        super().__init__(texto)

class VolverMenu(Exception):
    def __init__(self):
        texto = "Volviendo al Menú"
        super().__init__(texto)
