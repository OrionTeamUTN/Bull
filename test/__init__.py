import unittest
from app import create_app, db
from datetime import datetime
from app.services.account_services import AccountService
from app.services.coin_services import CoinServices
from app.services.wallet_services import WalletServices


class BaseTestClass(unittest.TestCase):
   
    def setUp(self):

        date = datetime(2000, 1, 1)
    
         # Datos para grabar en la db
        self.account_1_data = {
        "username": 'user_admin',
        "password": 'Abc1234',
        "email": 'admin@example.com',
        "first_name": 'Maria',
        "last_name": 'Perez',
        "phone": '2615777777',
        "address": 'Fake St. 123',
        "dni": 12345678,
        "birthdate": date,
        "is_admin": True
    }
        self.account_2_data = {
        "username": 'user_guest',
        "password": 'Xyz5678',
        "email": 'guest@example.com',
        "first_name": 'Jose',
        "last_name": 'Perez',
        "phone": '2615777757',
        "address": 'Fake St. 123',
        "dni": 87654321,
        "birthdate": date,
        "is_admin": False
    }
    # Datos falsos para romper test, no se graban en db
        self.fake_account = {
        "username": 'user_guest_2',
        "password": '3w4e5r',
        "email": 'no_admin@example.com',
        "first_name": 'Raul',
        "last_name": 'Perez',
        "phone": '2615555555',
        "address": 'Fake St. 123',
        "dni": 18273645,
        "birthdate": date,
        "is_admin": False
    }

        self.coin_data_1 = {
             "coin_name": "Bitcoin",
             "coin_symbol": "BTC",
             "is_active": False
        }
        self.coin_data_2 = {
             "coin_name": "Tether",
             "coin_symbol": "USDT",
        }
        self.coin_data_3 = {
             "coin_name": "Peronia",
             "coin_symbol": "PNA",
             "is_active": False
        }

        # Define test variables and initialize app
        # Crea un contexto de aplicación
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Crea las tablas de la base de datos
        db.create_all()
        #   ---- CREO CASOS PARA LAS RELACIONES DE CLAVE FORÁNEA ----
        # Creamos un usuario administrador
        self.acc_1 = self.create_account(self.account_1_data)
        # Creamos un usuario normal
        self.acc_2 = self.create_account(self.account_2_data)
        # Creamos coins para pruebas
        self.coin_1 = self.create_coin(self.coin_data_1, self.acc_1.id_account)
        self.coin_2 = self.create_coin(self.coin_data_2, self.acc_1.id_account)
        self.coin_3 = self.create_coin(self.coin_data_3, self.acc_1.id_account)
        # Creamos wallets para pruebas
        self.wall_1 = self.create_wallet(self.acc_1.id_account, self.coin_1.id_coin)
        self.wall_2 = self.create_wallet(self.acc_2.id_account, self.coin_2.id_coin)
        self.wall_3 = self.create_wallet(self.acc_2.id_account, self.coin_3.id_coin)
        

        

    def tearDown(self):
        # Elimina todas las bases de datos cuando termina
            db.session.remove()
            db.drop_all()
        


    @staticmethod
    #args(username, password, email, first_name, last_name, phone, address, dni, birthdate, is_admin)
    def create_account(account):
        service = AccountService()
        return service.save(account)

    @staticmethod
    # args(coin_name, coin_abbreviation)
    def create_coin(coin, admin_id):
        services = CoinServices()
        return services.save(coin, admin_id)

    @staticmethod
    # args(balance, id_owner_account, id_wallet_coin)
    def create_wallet(id_acc: int, id_coin: int):
        service = WalletServices()
        return service.save(id_acc, id_coin)
