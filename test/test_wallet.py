import unittest
from flask import current_app
from app import create_app

from app.models import Wallet
from datetime import datetime
from app.models import Account

class WalletTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
        # Datos de prueba
        self.ID_WALLET = 1
        self.BALANCE = 500
        self.ID_OWNER_ACCOUNT = 2

        self.ID_ACCOUNT = 2
        self.USERNAME_PRUEBA = 'test'
        self.EMAIL_PRUEBA = 'test@test.com'
        self.PASSWORD_PRUEBA = 'test1234'
        self.IS_ADMIN_PRUEBA = False
        self.SURNAME_PRUEBA = 'surname'
        self.ADDRESS_PRUEBA = 'address 1234'
        self.PHONE_PRUEBA = '542605502105'
        self.DNI_PRUEBA = 554872256
        self.BIRTHDATE_PRUEBA = datetime(2001, 2, 1)
       
    def tearDown(self):
        self.app_context.pop()

    def test_wallet(self):
    
        wallet = Wallet()
        
        wallet.id_wallet = self.ID_WALLET
        wallet.balance = self.BALANCE
        wallet.id_owner_account = self.ID_OWNER_ACCOUNT
        
        self.assertTrue(wallet.id_wallet,self.ID_WALLET) #Este comando verifica que ambos sean iguales
        self.assertTrue(wallet.balance, self.BALANCE)
        self.assertTrue(wallet.id_owner_account,self.ID_OWNER_ACCOUNT)

        
if __name__ == "__main__":
    unittest.main()