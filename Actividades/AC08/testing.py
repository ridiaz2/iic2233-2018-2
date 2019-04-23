import unittest
from dccontrolador import *

###############################################################################
"""
Tests
Acá escribe los test pedidos.
"""
class Testeo(unittest.TestCase):
    def test_caracter_invalido(self):
        self.assertRaises(ValueError,
            Supermercado("SuperPrueba").agregar_producto, "hola&", "producto")

    def test_in(self):
        producto_1, producto_2 = Producto("p1", 1), Producto("p2", 2)
        super1 = Supermercado("Super1")
        super1.agregar_producto("01", producto_1)
        super1.agregar_producto("02", producto_2)
        self.asser



###############################################################################

if __name__ == '__main__':
    unittest.main()
