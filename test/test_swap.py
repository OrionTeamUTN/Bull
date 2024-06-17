import unittest
from app import create_app
from app import db

from app.models import Swap, Account, Wallet, Coin
from app.services.account_services import accountservice
from app.services.coin_services import coinservices
from app.services.wallet_services import walletservices
from app.services.swap_service import SwapService
from datetime import datetime

# Servicios de cuenta y usuario
account_service = accountservice()
coin_service = coinservices()
wallet_service = walletservices()
swap_service = SwapService()

class SwapTestCase(unittest.TestCase):

    def setUp(self):

        # DATOS DE PRUEBA
        # Datos de account
        self.account_test_data = {
            "id_account": 2,
            "username": "test",
            "email": "test@test.com",
            "password": "test1234",
            "is_admin": False,
            "surname": "surname1",
            "address": "calle falsa 123",
            "phone": "542605502105",
            "dni": 554872256,
            "birthdate": datetime(2001,2,1)
        }

        # Datos de coin: bitcoin
        self.coin1_test_data = {
            "id_coin": 1,
            "coin_name": "bitcoin",
            "coin_abbreviation": "btc"
        }

        # Datos de coin: ethereum
        self.coin2_test_data = {
            "id_coin": 2,
            "coin_name": "ethereum",
            "coin_abbreviation": "eth"
        }

        # Datos de wallet
        self.wallet1_test_data = {
            "balance": 500,
            "id_owner_account": 2,
            "id_wallet_coin": 1
        }

        self.wallet2_test_data = {
            "balance": 0,
            "id_owner_account": 2,
            "id_wallet_coin": 2
        }

        # Datos de swap
        self.swap_test_data ={
            "operation_date": datetime.utcnow(),
            "amount_in": 400,
            "amount_out": 60,
            "id_wallet_in": 1,
            "id_wallet_out": 2
        }

        # Creamos la app y establecemos un contexto de aplicación (necesario para crear las tablas de la BD) <<aun debo investigar bien esto>>
        self.app = create_app() 
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all() # Creamos las tablas en la base de datos

    def tearDown(self):
        # Borramos los datos insertados y las tablas
        db.session.remove()
        db.drop_all()

    """ Test del objeto swap """
    def test_swap_as_object(self):
        swap = Swap(**self.swap_test_data)
        self.assertIsNone(swap.id_swap)
        self.assertTrue(swap.operation_date, self.swap_test_data["operation_date"])
        self.assertTrue(swap.amount_in, self.swap_test_data["amount_in"])
        self.assertTrue(swap.amount_out, self.swap_test_data["amount_out"])
        self.assertTrue(swap.id_wallet_in, self.swap_test_data["id_wallet_in"])
        self.assertTrue(swap.id_wallet_out, self.swap_test_data["id_wallet_out"])

    """ Test de guardar un registro de swap a la BD """
    def test_insert_swap_db(self):
        self.__insert_data_db() # insertamos los datos de prueba a la bd

        swap1 = Swap(**self.swap_test_data)
        swap_service.save(swap1)
    

    """ Test de obtener una lista de todos los registros swaps """
    def test_get_all_swaps(self):
        self.__insert_data_db()
        swap1 = Swap(**self.swap_test_data)
        self.swap_test_data["amount_in"] = 300
        self.swap_test_data["operation_date"] = datetime(2024,5,17)
        swap2 = Swap(**self.swap_test_data)
        self.swap_test_data["amount_out"] = 450
        self.swap_test_data["operation_date"] = datetime(2024,7,9)
        swap3 = Swap(**self.swap_test_data)

        # insertamos los tres swaps
        swap_service.save(swap1)
        swap_service.save(swap2)
        swap_service.save(swap3)

        l_swaps = swap_service.get_all()
        #print(l_swaps)
        self.assertIsNotNone(l_swaps)

    """ Test de buscar un swap por su id """
    def test_find_by_id(self):
        self.__insert_data_db()
        swap1 = Swap(**self.swap_test_data)
        swap2 = Swap(**self.swap_test_data)
        swap3 = Swap(**self.swap_test_data)

        swap_service.save(swap1)
        swap_service.save(swap2)
        swap_service.save(swap3)

        finded_swap1 = swap_service.find_by_id(1)
        finded_swap2 = swap_service.find_by_id(2)
        finded_swap3 = swap_service.find_by_id(3)
        finded_swap5 = swap_service.find_by_id(5)
        self.assertEqual(finded_swap1, swap1)
        self.assertEqual(finded_swap2, swap2)
        self.assertEqual(finded_swap3, swap3)
        self.assertIsNone(finded_swap5) # el swap con id 5 no debería existir, por lo que debe ser None


    """ Test de filtrar registros de swaps por una wallet en específico """
    def test_filter_by_wallet_id(self):
        self.__insert_data_db()
        
        # Creamos otra moneda, para otra billetera
        other_coin_data = {
            "id_coin": 3,
            "coin_name": "Dogecoin",
            "coin_abbreviation": "DOGE"
        }
        other_coin = Coin(**other_coin_data)
        coin_service.save(other_coin)

        self.wallet1_test_data["id_wallet_coin"] = 3 # asignamos la id de la nueva moneda
        other_wallet = Wallet(**self.wallet1_test_data)
        wallet_service.save(other_wallet)

        # swap donde wallet 1 envía a wallet 2
        swap1 = Swap(**self.swap_test_data) 

        # wallet 1 envía a wallet 3
        self.swap_test_data["amount_in"] = 700
        self.swap_test_data["id_wallet_out"] = 3
        swap2 = Swap(**self.swap_test_data) 

        # wallet 2 envía a wallet 1
        self.swap_test_data["id_wallet_in"] = 2
        self.swap_test_data["id_wallet_out"] = 1
        self.swap_test_data["amount_in"] = 10
        swap3 = Swap(**self.swap_test_data) 

        # wallet 2 envía a wallet 3
        self.swap_test_data["id_wallet_in"] = 2
        self.swap_test_data["id_wallet_out"] = 3
        self.swap_test_data["amount_in"] = 50
        swap4 = Swap(**self.swap_test_data) 

        swap_service.save(swap1)
        swap_service.save(swap2)
        swap_service.save(swap3)
        swap_service.save(swap4)

        swaps_of_wallet1 = swap_service.filter_by_wallet_id(1)
        self.assertIsNotNone(swaps_of_wallet1)
        self.assertEqual(len(swaps_of_wallet1), 3) # Deben haber solo tres registros donde wallet 1 esté involucrado
        swaps_of_wallet2 = swap_service.filter_by_wallet_id(2)
        self.assertIsNotNone(swaps_of_wallet2)
        self.assertEqual(len(swaps_of_wallet2), 3)
        swaps_of_wallet3 = swap_service.filter_by_wallet_id(3)
        self.assertIsNotNone(swaps_of_wallet3)
        self.assertEqual(len(swaps_of_wallet3), 2) 

        swaps_of_wallet4 = swap_service.filter_by_wallet_id(5) # Una billetera inexistente o bien que no haya tenido ningun swap
        self.assertIsNone(swaps_of_wallet4)


    """ Función que inserta los datos de prueba (cuenta, moneda y billetera) a la BD. Para utilizar en los test """
    def __insert_data_db(self):
        # Creamos una cuenta, dos modenas y dos billeteras previamente insertando a la BD
        account1 = Account(**self.account_test_data)
        coin1 = Coin(**self.coin1_test_data)
        coin2 = Coin(**self.coin2_test_data)
        wallet1 = Wallet(**self.wallet1_test_data)
        wallet2 = Wallet(**self.wallet2_test_data)

        # Insertamos en la BD
        account_service.save(account1)
        coin_service.save(coin1)
        coin_service.save(coin2)
        wallet_service.save(wallet1)
        wallet_service.save(wallet2)

if __name__ == "__main__":
    unittest.main()