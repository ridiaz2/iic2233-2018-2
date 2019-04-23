import re
from funciones import comprobar_correo, comprobar_password, entrada, verificar
from excepciones import Volver, VolverMenu
from web_service import consulta




'''
correo = "hla@g.oooooooooo"
password = "kdkdkdAA"

if comprobar_correo(correo):
    print(True)
else:
    print(False)

if comprobar_password(password):
    print(True)
else:
    print(False)
'''


if __name__ == '__main__':
    while True:
        try:
            print("_"*80)
            print("Bienvenid@ a DCConect :D")
            print("_"*80)
            print("A continuación puedes ingresar tus datos:")
            correo = verificar(">>> Correo: ", comprobar_correo)
            password = verificar(">>> Contraseña: ", comprobar_password)
            print("¡Ingreso exitoso!")
            consulta()



        except Volver:
            pass

        except VolverMenu:
            pass
