import unittest
from secuencial import buscar_secuencial
from binaria import buscar_binaria
from hash_busqueda import buscar_hash


class Pruebas(unittest.TestCase):
    def test_secuencial(self):
        self.assertEqual(buscar_secuencial(['b', 'a'], 'a'), 1)
        self.assertEqual(buscar_secuencial(['b'], 'a'), -1)
        self.assertEqual(buscar_secuencial([], 'a'), -1)

    def test_binaria(self):
        for i, valor in enumerate([2, 4, 6, 8, 10]):
            self.assertEqual(buscar_binaria([2, 4, 6, 8, 10], valor), i)
        self.assertEqual(buscar_binaria([2, 4, 6], 5), -1)
        self.assertEqual(buscar_binaria([], 1), -1)

    def test_hash(self):
        self.assertEqual(buscar_hash({'ana': '555-0101'}, 'ana'), '555-0101')
        self.assertIsNone(buscar_hash({'ana': '555-0101'}, 'luis'))
        self.assertIsNone(buscar_hash({}, 'ana'))


if __name__ == '__main__':
    unittest.main()
