import unittest
from app import create_app
from app import db

from app.models import Swap, Account, Wallet, Coin
from app.services.account_services import AccountService
from app.services.coin_services import CoinServices
from app.services.wallet_services import WalletServices
from app.services.swap_service import SwapService
from datetime import datetime

# Servicios de cuenta y usuario
account_service = AccountService()
coin_service = CoinServices()
wallet_service = WalletServices()
swap_service = SwapService()

class SwapTestCase(unittest.TestCase):

    def setUp(self):

        # DATOS DE PRUEBA
        # Datos de account
        self.account_test_data = {
            "id_account": 1,
            "username": "test",
            "password": "test1234",
            "email": "test@test.com",
            "first_name": "Cristian",
            "last_name": "Donozo",
            "phone": "542605502105",
            "address": "calle falsa 123",
            "dni": 554872256,
            "birthdate": datetime(2001,2,1),
            "is_admin": True
        }

        # Datos de coin: bitcoin
        self.coin1_test_data = {
            "id_coin": 1,
            "coin_name": "bitcoin",
            "coin_symbol": "btc"
        }

        # Datos de coin: ethereum
        self.coin2_test_data = {
            "id_coin": 2,
            "coin_name": "ethereum",
            "coin_symbol": "eth"
        }

        # Datos de wallet
        self.wallet1_test_data = {
            "id_owner_account": 2,
            "id_wallet_coin": 1
        }

        self.wallet2_test_data = {
            "id_owner_account": 2,
            "id_wallet_coin": 2
        }

        # Datos de swap
        self.swap_test_data ={
            "operation_date": datetime.today(),
            "amount_send": 100,
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
        #self.assertTrue(swap.amount_recv, self.swap_test_data["amount_recv"])
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

        # Verificamos el balance de la billetera que envía antes y despues del swap
        print(f"Balance antes de hacer el swap:  {wallet_service.find_by_id(1).balance} {wallet_service.find_by_id(1).coin.coin_symbol}")
        self.assertEqual(wallet_service.find_by_id(1).balance, 700) 
        swap_service.save(swap1)
        print(f"Balance luego de hacer el swap:  {wallet_service.find_by_id(1).balance} {wallet_service.find_by_id(1).coin.coin_symbol}")
        self.assertEqual(wallet_service.find_by_id(1).balance, 600)

        # Monto recibido:
        print(f"Monto recibido:  {swap1.amount_recv} {swap1.wallet_recv.coin.coin_symbol}")

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
        self.swap_test_data['amount_send'] = 1000
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
    def __test_filter_by_wallet(self):
        self.__insert_data_db()
        
        # Creamos otra moneda, para otra billetera
        other_coin_data = {
            "id_coin": 3,
            "coin_name": "Dogecoin",
            "coin_symbol": "DOGE"
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
        self.assertNotEqual(swaps_wallet1_send, [])
        self.assertEqual(len(swaps_wallet1_send), 2) # Dos swaps donde la wallet 1 envía coins
        swaps_wallet1_recv = swap_service.filter_by_wallet_recv(1)
        self.assertNotEqual(swaps_wallet1_recv, [])
        self.assertEqual(len(swaps_wallet1_recv), 1) # Un swap donde wallet 1 envía coins

        swaps_wallet2_send = swap_service.filter_by_wallet_send(2)
        self.assertNotEqual(swaps_wallet2_send, [])
        self.assertEqual(len(swaps_wallet2_send), 2) # Dos swaps donde wallet 2 envía coins
        swaps_wallet2_recv = swap_service.filter_by_wallet_recv(2)
        self.assertNotEqual(swaps_wallet2_recv, [])
        self.assertEqual(len(swaps_wallet2_recv),1) # Un swap donde wallet 2 recibe coins

        swaps_wallet3_send = swap_service.filter_by_wallet_send(3)
        self.assertEqual(swaps_wallet3_send, []) # La wallet 3 no tiene swaps en los que haya enviado coins, por lo que debe ser None
        swaps_wallet3_recv = swap_service.filter_by_wallet_recv(3)
        self.assertNotEqual(swaps_wallet3_recv, [])
        self.assertEqual(len(swaps_wallet3_recv), 2) # Tiene dos swaps en los que recibe coins.

        swaps_wallet4_send = swap_service.filter_by_wallet_send(5) # Una wallet inexistente o bien que no haya tenido ningun swap
        self.assertEqual(swaps_wallet4_send, [])

    """ Test que filtra swaps por fecha de operación """
    def __test_filter_by_op_date(self):
        self.__insert_data_db()
        fecha_hoy = datetime.today()
        fecha_uno = datetime(2024, 6, 15)
        fecha_dos = datetime(2024, 5, 17)

        swap1 = Swap(**self.swap_test_data)
        
        self.swap_test_data["operation_date"] = fecha_uno
        swap2 = Swap(**self.swap_test_data)

        swap_service.save(swap1)
        swap_service.save(swap2)

        swaps_all = swap_service.get_all()
        swaps_hoy = swap_service.filter_by_op_date(swaps_all, fecha_hoy) # Debería ser el primero que creamos con la fecha de hoy
        self.assertIsNotNone(swaps_hoy)
        self.assertEqual(swaps_hoy, [swap1]) 
        swaps_fecha_uno = swap_service.filter_by_op_date(swaps_all, fecha_uno) # Debería ser el segundo que creamos
        self.assertIsNotNone(swaps_fecha_uno)
        self.assertEqual(swaps_fecha_uno, [swap2])
        swaps_fecha_dos = swap_service.filter_by_op_date(swaps_all, fecha_dos) # No existe ningún swap realizado en esta fecha.
        self.assertIsNone(swaps_fecha_dos)

    
    def __test_filter_by_wallet_at_opdate(self):
        self.__insert_data_db()

        swap1 = Swap(**self.swap_test_data)
        
        swap_service.save(swap1)
        swaps_wallet_1 = swap_service.find_by_op_date_and_wallet(datetime.today(), 1)
        self.assertNotEqual(swaps_wallet_1, []) # Distinto a una lista vacía


    """ Método (no test) que inserta los datos de prueba (cuenta, moneda y billetera) a la BD. Para utilizar en los test """
    def __insert_data_db(self):

        # Insertamos en la BD
        account_service.save(self.account_test_data)
        coin_service.save(admin_id=1, args=self.coin1_test_data)
        coin_service.save(admin_id=1, args=self.coin2_test_data)
        wallet_service.save(acc_id=1, coin_id=1)
        wallet_service.save(acc_id=1, coin_id=2)

        # Asignamos balance a las billeteras
        wallet_service.update(wallet_id=1, balance=700)
        wallet_service.update(wallet_id=2, balance=200)


if __name__ == "__main__":
    unittest.main()