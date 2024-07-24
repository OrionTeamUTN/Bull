import unittest
from . import BaseTestClass as base_t
from app.services.coin_services import CoinServices
from app.models.coin import Coin

class CointTestCase(base_t):

    # Función para recorrer el diccionario por cada uno de sus atributos
    # para poder compararlos con el objeto almacenado en la DB
    def compare_two_true(self, coin_1: dict, coin_2: Coin):
        for key in coin_1.keys():
            self.assertEqual(coin_1[key], getattr(coin_2, key))

    # Realiza las mismas funciones de la anterior pero esta vez compara que dos
    # elementos no sean iguales
    def compare_two_false(self, coin_1: dict, coin_2: Coin):
        for key in coin_1.keys():
            self.assertNotEqual(coin_1[key], getattr(coin_2, key))
        
    coin_serv = CoinServices()

    # Test para probar función save
    def test_save(self):
        coin_1 = self.coin_serv.save(self.coin_data_1, self.acc_1.id_account)
        coin_2 = self.coin_serv.save(self.coin_data_2, self.acc_2.id_account)

        self.compare_two_true(self.coin_data_1, coin_1)
        self.compare_two_false(self.coin_data_2, coin_1)
        self.assertEqual(coin_2, "No tiene permiso para realizar esta acción")

    # Test para probar función update
    def test_update(self):
        coin_1 = self.coin_serv.update(self.coin_1.id_coin, self.acc_1.id_account)
        coin_2 = self.coin_serv.update(self.coin_2.id_coin, self.acc_2.id_account)

        self.assertNotEqual(self.coin_data_1['is_active'], coin_1.is_active)
        self.assertEqual(coin_2, "No tiene permiso para realizar esta acción")

    # Test para probar funcionalidad de get_all
    def test_get_all(self):
        res = self.coin_serv.get_all()

        self.compare_two_true(self.coin_data_1, res[0])
        self.compare_two_true(self.coin_data_2, res[1])

    # Test para probar la funcionalidad de find_by_id
    def test_find_by_id(self):
        res_1 = self.coin_serv.find_by_id(1)
        res_2 = self.coin_serv.find_by_id(2)

        self.compare_two_true(self.coin_data_1, res_1)
        self.compare_two_true(self.coin_data_2, res_2)
        self.compare_two_false(self.coin_data_1, res_2)

    # Test para probar la funcionalidad de find_by_name
    def test_find_by_name(self):
        res_1 = self.coin_serv.find_by_name(self.coin_data_1['coin_name'])
        res_2 = self.coin_serv.find_by_name(self.coin_data_2['coin_name'])
        res_3 = self.coin_serv.find_by_name('Pepe')

        self.assertEqual(res_1.coin_name, self.coin_data_1['coin_name'])
        self.assertEqual(res_2.coin_name, self.coin_data_2['coin_name'])
        self.assertEqual(res_3, "Coin not found - 404")

    # Test para probar la funcionalidad de find_by_symbol
    def test_find_by_symbol(self):
        res_1 = self.coin_serv.find_by_symbol(self.coin_data_1['coin_symbol'])
        res_2 = self.coin_serv.find_by_symbol(self.coin_data_2['coin_symbol'])
        res_3 = self.coin_serv.find_by_symbol('P$p%')

        self.assertEqual(res_1.coin_symbol, self.coin_data_1['coin_symbol'])
        self.assertEqual(res_2.coin_symbol, self.coin_data_2['coin_symbol'])
        self.assertEqual(res_3, "Coin not found - 404")

    # Test para probar la funcionalidad de buscar las monedas que estan activas
    def test_find_by_is_active(self):
        res = self.coin_serv.get_active_coins()
        self.compare_two_true(self.coin_data_2, res[0])

    # Test para probar la funcionalidad de buscar las monedas que estan inactivas
    def test_find_by_is_inactive(self):
        res = self.coin_serv.get_inactive_coins() 
        self.compare_two_true(self.coin_data_1, res[0])
        self.compare_two_true(self.coin_data_3, res[1])

    # Test para probar funcionalidad de delete
    def test_delete(self):
        res_1 = self.coin_serv.delete(self.coin_2.id_coin, 1)
        res_2 = self.coin_serv.delete(self.coin_1.id_coin, 4)

        self.assertEqual(res_1, "Success")
        self.assertEqual(res_2, "No tiene permiso para realizar esta acción")


if __name__ == '__main__':
    unittest.main()