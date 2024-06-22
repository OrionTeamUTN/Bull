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
            "balance": 200,
            "id_owner_account": 2,
            "id_wallet_coin": 2
        }

        # Datos de swap
        self.swap_test_data ={
            "operation_date": datetime.utcnow(),
            "amount_send": 100,
            "amount_recv": 60,
            "id_wallet_send": 1, # a wallet1
            "id_wallet_recv": 2  # a wallet2
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
        self.assertTrue(swap.amount_send, self.swap_test_data["amount_send"])
        self.assertTrue(swap.amount_recv, self.swap_test_data["amount_recv"])
        self.assertTrue(swap.id_wallet_send, self.swap_test_data["id_wallet_send"])
        self.assertTrue(swap.id_wallet_recv, self.swap_test_data["id_wallet_recv"])
        
        # Testeamos también los relationship, en este punto debe retornar None debido solo se crea un objeto Swap y no existen las instancias relacionadas
        self.assertIsNone(swap.wallet_send)
        self.assertIsNone(swap.wallet_recv)

    """ Test de guardar un registro de swap a la BD """
    def test_insert_swap_db(self):
        self.__insert_data_db() # insertamos los datos de prueba a la bd, requeridos para que un swap esté relacionado.

        swap1 = Swap(**self.swap_test_data)
        # Antes de insertar a la BD, probamos las relaciones
        self.assertIsNone(swap1.wallet_send) # Resultan None puesto que aun no se ha insertado el swap a la BD
        self.assertIsNone(swap1.wallet_recv)

        swap_service.save(swap1)

        # Probamos otra vez
        self.assertIsNotNone(swap1.wallet_send)
        self.assertIsNotNone(swap1.wallet_recv)
        self.assertIsInstance(swap1.wallet_send, Wallet)
        # Ahora que está insertado en la BD sí nos trae las relaciones
    
    """ Test de swap con wallet_send inexistente """
    def test_unexisting_wallet_send(self):
        self.__insert_data_db()
        self.swap_test_data['id_wallet_send'] = 5

        swap = Swap(**self.swap_test_data)
        self.assertIsNone(swap_service.save(swap))

    """ Test de swap con monto enviado invalido, superior al balance de la wallet """
    def test_invalid_amount_send(self):
        self.wallet1_test_data['balance'] = 300 
        self.swap_test_data['amount_send'] = 350
        self.__insert_data_db()

        swap = Swap(**self.swap_test_data)
        self.assertIsNone(swap_service.save(swap))


    """ Test de obtener una lista de todos los registros swaps """ 
    def test_get_all_swaps(self):
        self.__insert_data_db()
        swap1 = Swap(**self.swap_test_data)
        self.swap_test_data["amount_send"] = 300
        self.swap_test_data["operation_date"] = datetime(2024,5,17)
        swap2 = Swap(**self.swap_test_data)
        self.swap_test_data["amount_recv"] = 450
        self.swap_test_data["operation_date"] = datetime(2024,7,9)
        swap3 = Swap(**self.swap_test_data)

        # insertamos los tres swaps
        swap_service.save(swap1)
        swap_service.save(swap2)
        swap_service.save(swap3)

        l_swaps = swap_service.get_all()
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
    def test_filter_by_wallet(self):
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

        # swap donde wallet (1) envía a wallet (2)
        swap1 = Swap(**self.swap_test_data) 

        # wallet (1) envía a wallet (3)
        self.swap_test_data["amount_send"] = 100
        self.swap_test_data["id_wallet_recv"] = 3
        swap2 = Swap(**self.swap_test_data) 

        # wallet (2) envía a wallet (1)
        self.swap_test_data["id_wallet_send"] = 2
        self.swap_test_data["id_wallet_recv"] = 1
        self.swap_test_data["amount_send"] = 10
        swap3 = Swap(**self.swap_test_data) 

        # wallet (2) envía a wallet (3)
        self.swap_test_data["id_wallet_send"] = 2
        self.swap_test_data["id_wallet_recv"] = 3
        self.swap_test_data["amount_send"] = 50
        swap4 = Swap(**self.swap_test_data) 

        swap_service.save(swap1)
        swap_service.save(swap2)
        swap_service.save(swap3)
        swap_service.save(swap4)


        swaps_wallet1_send = swap_service.filter_by_wallet_send(1)
        self.assertIsNotNone(swaps_wallet1_send)
        self.assertEqual(len(swaps_wallet1_send), 2) # Dos swaps donde la wallet 1 envía coins
        swaps_wallet1_recv = swap_service.filter_by_wallet_recv(1)
        self.assertIsNotNone(swaps_wallet1_recv)
        self.assertEqual(len(swaps_wallet1_recv), 1) # Un swap donde wallet 1 envía coins

        swaps_wallet2_send = swap_service.filter_by_wallet_send(2)
        self.assertIsNotNone(swaps_wallet2_send)
        self.assertEqual(len(swaps_wallet2_send), 2) # Dos swaps donde wallet 2 envía coins
        swaps_wallet2_recv = swap_service.filter_by_wallet_recv(2)
        self.assertIsNotNone(swaps_wallet2_recv)
        self.assertEqual(len(swaps_wallet2_recv),1) # Un swap donde wallet 2 recibe coins

        swaps_wallet3_send = swap_service.filter_by_wallet_send(3)
        self.assertIsNone(swaps_wallet3_send) # La wallet 3 no tiene swaps en los que haya enviado coins, por lo que debe ser None
        swaps_wallet3_recv = swap_service.filter_by_wallet_recv(3)
        self.assertIsNotNone(swaps_wallet3_recv)
        self.assertEqual(len(swaps_wallet3_recv), 2) # Tiene dos swaps en los que recibe coins.

        swaps_wallet4_send = swap_service.filter_by_wallet_send(5) # Una wallet inexistente o bien que no haya tenido ningun swap
        self.assertIsNone(swaps_wallet4_send)

    """ Test que filtra swaps por fecha de operación """
    def test_filter_by_op_date(self):
        self.__insert_data_db()
        fecha_hoy = datetime.utcnow()
        fecha_uno = datetime(2024, 6, 15)
        fecha_dos = datetime(2024, 5, 17)

        swap1 = Swap(**self.swap_test_data)
        
        self.swap_test_data["operation_date"] = fecha_uno
        swap2 = Swap(**self.swap_test_data)

        swap_service.save(swap1)
        swap_service.save(swap2)

        swaps_hoy = swap_service.filter_by_op_date(fecha_hoy) # Debería ser el primero que creamos con la fecha de hoy
        self.assertIsNotNone(swaps_hoy)
        self.assertEqual(swaps_hoy, [swap1]) 
        swaps_fecha_uno = swap_service.filter_by_op_date(fecha_uno) # Debería ser el segundo que creamos
        self.assertIsNotNone(swaps_fecha_uno)
        self.assertEqual(swaps_fecha_uno, [swap2])
        swaps_fecha_dos = swap_service.filter_by_op_date(fecha_dos) # No existe ningún swap realizado en esta fecha.
        self.assertIsNone(swaps_fecha_dos)

    """ Método (no test) que inserta los datos de prueba (cuenta, moneda y billetera) a la BD. Para utilizar en los test """
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