import unittest
from flask import current_app
from app import create_app, db
from app.models import Coin
from app.models import Wallet
from app.models import Account
from datetime import datetime
from app.services.wallet_services import walletservices
from app.services.account_services import accountservice
from app.services.coin_services import coinservices 

account_service = accountservice()

coin_service= coinservices()

wallet_services = walletservices()

class WalletTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
        # Datos de prueba
        # Datos Billetera
        self.ID_WALLET = 1
        self.BALANCE = 500
        self.ID_OWNER_ACCOUNT = 2
        self.ID_WALLET_COIN= 1

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
        
        self.ID_COIN = 1
        self.NAME = 'bitcoin'
        self.COIN_ABBREVATION = 'btc'
        self.ID_COIN_WALLET = 1
        
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
       
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_wallet_save(self):
        coin = self.__get_coin()
        coin_service.save(coin)
        self.assertGreaterEqual(coin.id_coin, 1)
        self.assertEqual(coin.coin_abbreviation, self.COIN_ABBREVATION)
        
        
        account = self.__get_account()
        
        account_service.save(account)
        
        self.assertGreaterEqual(account.id_account, 2)
        self.assertEqual(account.email, self.EMAIL_PRUEBA)
        self.assertEqual(account.username, self.USERNAME_PRUEBA)
        self.assertIsNotNone(account.password)
        self.assertTrue(account_service.check_auth(account.dni, self.PASSWORD_PRUEBA))
        self.assertEqual(account.surname, self.SURNAME_PRUEBA)
        self.assertEqual(account.address, self.ADDRESS_PRUEBA)
        self.assertEqual(account.phone, self.PHONE_PRUEBA)
        self.assertEqual(account.dni, self.DNI_PRUEBA)  
        wallett = self.__get_wallet()
        wallet_services.save(wallett)
        self.assertGreaterEqual(wallett.id_wallet, 1)
        self.assertEqual(wallett.balance, self.BALANCE)
        self.assertEqual(wallett.id_owner_account, self.ID_OWNER_ACCOUNT)
        self.assertEqual(wallett.id_wallet_coin, self.ID_WALLET_COIN) 


    
    def test_account_delete(self):
        #se encarga de borrar la cuenta
      account = self.__get_account()
        
      account_service.save(account)

      account_service.delete(account)
        
      self.assertIsNone(account_service.find(account))


    def __get_wallet(self):
        wallet = Wallet()
        wallet.id_wallet = self.ID_WALLET
        wallet.balance = self.BALANCE
        wallet.id_owner_account = self.ID_OWNER_ACCOUNT   
        wallet.id_wallet_coin = self.ID_WALLET_COIN
        return wallet   
    
    def __get_account(self):
        data = Account()
        data.id_account= self.ID_ACCOUNT
        data.surname=self.SURNAME_PRUEBA
        data.address=self.ADDRESS_PRUEBA
        data.phone=self.PHONE_PRUEBA
        data.dni=self.DNI_PRUEBA
        data.birthdate=self.BIRTHDATE_PRUEBA
        
        data.username=self.USERNAME_PRUEBA
        data.email=self.EMAIL_PRUEBA
        data.password=self.PASSWORD_PRUEBA  
        data.is_admin=self.IS_ADMIN_PRUEBA
        

        return data

    def __get_coin(self):
        coin = Coin()
        coin.id_coin = self.ID_COIN
        coin.coin_abbreviation = self.COIN_ABBREVATION
        coin.id_coin_wallet = self.ID_COIN_WALLET
        return coin   
    
if __name__ == "__main__":
    unittest.main()