import unittest
from . import BaseTestClass as base_t
from app.services.wallet_services import WalletServices

class WalletTestCase(base_t):

    wall_srvs = WalletServices()

    # Test para probar que guarda la wallet
    def test_save(self):
        res_1 = self.wall_srvs.save(self.acc_1.id_account, self.coin_1.id_coin)
        res_2 = self.wall_srvs.save(self.acc_2.id_account, self.coin_2.id_coin)
        # A las siguientes se les pasa datos inexistentes para que fallen
        res_3 = self.wall_srvs.save(4, self.coin_2.id_coin)
        res_4 = self.wall_srvs.save(self.acc_2.id_account, 4)
        self.assertEqual(res_1.id_owner_account, self.acc_1.id_account)
        self.assertEqual(res_1.id_wallet_coin, self.coin_1.id_coin)
        self.assertEqual(res_2.id_owner_account, self.acc_2.id_account)
        self.assertEqual(res_2.id_wallet_coin, self.coin_2.id_coin)
        self.assertIsNone(res_3)
        self.assertIsNone(res_4)

    # Test para probar que borra una wallet
    def test_delete(self):
        res_1 = self.wall_srvs.delete(self.wall_2.id_wallet)
        self.assertEqual(res_1, "Deleted")

    # Test para probar que actualiza el saldo de la wallet
    def test_update(self):
        res_1 = self.wall_srvs.update(self.wall_1.id_wallet, 500)
        res_2 = self.wall_srvs.update(self.wall_1.id_wallet, -500)
        res_3 = self.wall_srvs.update(4, 500)
        
        self.assertEqual(res_1.balance, 500)
        self.assertEqual(res_2, "Balance cannot be negative")
        self.assertIsNone(res_3)

    # Test para probar que muestra todas las wallets de un usuario
    def test_get_all(self):
        res = self.wall_srvs.get_all()
        self.assertEqual(res[0], self.wall_1)
        self.assertEqual(res[1], self.wall_2)

    # Test para probar que encuentra una wallet por id, relacionada a un usuario
    def test_find_by_id(self):
        res_1 = self.wall_srvs.find_by_id(self.wall_1.id_wallet)
        res_2 = self.wall_srvs.find_by_id(4)
        self.assertEqual(res_1.id_wallet, self.wall_1.id_wallet)
        self.assertIsNone(res_2)

    # Test para probar que encuentra una wallet por nombre de su cripto, relacionada a un usuario
    def test_find_by_coin_name(self):
        res_1 = self.wall_srvs.find_by_coin_name(self.coin_1.coin_name)
        res_2 = self.wall_srvs.find_by_coin_name("Pame")
        self.assertEqual(res_1.id_wallet, self.wall_1.id_wallet)
        self.assertIsNone(res_2)

    # Test para probar que encuentra una wallet por el simbolo de su cripto, relacionada a un usuario
    def test_find_by_coin_symbol(self):
        res_1 = self.wall_srvs.find_by_coin_symbol(self.coin_1.coin_symbol)
        res_2 = self.wall_srvs.find_by_coin_symbol("bull")
        self.assertEqual(res_1.id_wallet, self.wall_1.id_wallet)
        self.assertIsNone(res_2)

    # Test para probar que muestra el balance de una wallet
    def test_check_balance(self):
        # Le agrego saldo a una wallet para probarla
        self.wall_srvs.update(self.wall_2.id_wallet, 500)

        res_1 = self.wall_srvs.check_balance(self.wall_2.id_wallet)
        res_2 = self.wall_srvs.check_balance(self.wall_3.id_wallet)
        res_3 = self.wall_srvs.check_balance(4)

        self.assertTrue(res_1)
        self.assertFalse(res_2)
        self.assertIsNone(res_3)

    # Test para retirar balance
    def test_withdraw(self):
        # Le agrego saldo a una wallet para probarla
        self.wall_srvs.update(self.wall_1.id_wallet, 5000)
        res_1 = self.wall_srvs.withdraw(self.wall_1.id_wallet, 1000)
        res_2 = self.wall_srvs.withdraw(self.wall_1.id_wallet, -1000)
        res_3 = self.wall_srvs.withdraw(4, 1000)
        res_4 = self.wall_srvs.withdraw(self.wall_2.id_wallet, 1000)

        self.assertEqual(res_1.balance, 4000)
        self.assertEqual(res_2, "Amount cannot be negative")
        self.assertIsNone(res_3)
        self.assertEqual(res_4, "Insufficient balance")

    # Test para probar que traiga todas las wallets que tienen balance >0
    def test_find_by_positive_balance(self):
        self.wall_srvs.update(self.wall_1.id_wallet, 5000)
        self.wall_srvs.update(self.wall_2.id_wallet, 5000)
        res_1 = self.wall_srvs.find_by_positive_balance()

        self.assertEqual(len(res_1), 2)
        self.assertEqual(res_1[0].id_wallet, self.wall_1.id_wallet)
        self.assertEqual(res_1[1].id_wallet, self.wall_2.id_wallet)

    # Test para probar que traiga todas las wallets que tienen balance = 0
    def test_find_by_zero_balance(self):
        res = self.wall_srvs.find_by_zero_balance()

        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].id_wallet, self.wall_1.id_wallet)
        self.assertEqual(res[1].id_wallet, self.wall_2.id_wallet)
        self.assertEqual(res[2].id_wallet, self.wall_3.id_wallet)

if __name__ == '__main__':
    unittest.main()