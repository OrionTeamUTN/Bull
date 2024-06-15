import unittest
from flask import current_app
from app import create_app, db
from app.models import Account
from datetime import datetime
from app.services.account_services import accountservice

account_service = accountservice()

class AccountTestCase(unittest.TestCase):

    def setUp(self):
        #definimos los valores de prueba los crea y los guarda en la base de datos, este metodo se llama para cada prueba que se ejecute
        #setUp es un metodo que incorpora unittest junto con tearDown 
        self.USERNAME_PRUEBA = 'test'
        self.EMAIL_PRUEBA = 'test@test.com'
        self.PASSWORD_PRUEBA = 'test1234'
        self.IS_ADMIN_PRUEBA = False
        self.SURNAME_PRUEBA = 'surname'
        self.ADDRESS_PRUEBA = 'address 1234'
        self.PHONE_PRUEBA = '542605502105'
        self.DNI_PRUEBA = 554872256
        self.BIRTHDATE_PRUEBA = datetime(2001, 2, 1)
        
        self.USERNAME_PRUEBA1 = 'tst1'
        self.EMAIL_PRUEBA1 = 'tst@test.com1'
        self.PASSWORD_PRUEBA1 = 'test12341'
        self.IS_ADMIN_PRUEBA1 = True
        self.SURNAME_PRUEBA1 = 'srname1'
        self.ADDRESS_PRUEBA1 = 'adress 12344'
        self.PHONE_PRUEBA1 = '54205502054'
        self.DNI_PRUEBA1 = 554872563
        self.BIRTHDATE_PRUEBA1 = datetime(2001, 2, 1)

        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        

    def tearDown(self):
        #Se encaraga de borrar los valores que pasamamos anteriormente, en la base datos.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)
    
    def test_account(self):
        
        account = self.__get_account()

        #con esto comprobamos que lso valores que se cargaron, son los mismos que pasamos.
        
        self.assertEqual(account.email, self.EMAIL_PRUEBA)
        self.assertEqual(account.username, self.USERNAME_PRUEBA)
        self.assertEqual(account.password, self.PASSWORD_PRUEBA)
        self.assertFalse(account.is_admin)
        self.assertEqual(account.surname, self.SURNAME_PRUEBA)
        self.assertEqual(account.address, self.ADDRESS_PRUEBA)
        self.assertEqual(account.phone, self.PHONE_PRUEBA)
        self.assertEqual(account.dni, self.DNI_PRUEBA)
        self.assertEqual(account.birthdate, self.BIRTHDATE_PRUEBA)

    def test_account_save(self):
        account = self.__get_account()
        
        account_service.save(account)
        
        self.assertGreaterEqual(account.id_account, 1)
        self.assertEqual(account.email, self.EMAIL_PRUEBA)
        self.assertEqual(account.username, self.USERNAME_PRUEBA)
        self.assertIsNotNone(account.password)
        self.assertTrue(account_service.check_auth(account.dni, self.PASSWORD_PRUEBA))
        self.assertEqual(account.surname, self.SURNAME_PRUEBA)
        self.assertEqual(account.address, self.ADDRESS_PRUEBA)
        self.assertEqual(account.phone, self.PHONE_PRUEBA)
        self.assertEqual(account.dni, self.DNI_PRUEBA)
        self.assertEqual(account.birthdate, self.BIRTHDATE_PRUEBA)
        
    
    def test_account_delete(self):
        #se encarga de borrar la cuenta
      account = self.__get_account()
        
      account_service.save(account)

      account_service.delete(account)
        
      self.assertIsNone(account_service.find(account))
    
    
    def test_account_find(self):
        #verifica que el metodo find funcione correctamente.
        account = self.__get_account()
        account_service.save(account)
  
        
        account_find= account_service.find(1)
        self.assertIsNotNone(account_find)
        self.assertEqual(account_find.id_account, account.id_account)
        
    def test_get_other_account (self):
        #verifica que le metodo para ver la informacion de otra cuenta funcione.
        account1 = self.__get_account()
        account = self.__get_account1()
        account_service.save(account1)
        account_service.save(account)
        
        self.assertTrue(account.is_admin)
        
        account_find1 = account_service.get_other_account_info(account1.dni, account.dni)
        self.assertIsNotNone(account_find1)
        self.assertEqual(account_find1.username, account1.username)
        self.assertEqual(account_find1.email , account1.email)
      

    def __get_account(self):
        data = Account()
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
    def __get_account1(self):
        data1 = Account()
        data1.surname=self.SURNAME_PRUEBA1
        data1.address=self.ADDRESS_PRUEBA1
        data1.phone=self.PHONE_PRUEBA1
        data1.dni=self.DNI_PRUEBA1
        data1.birthdate=self.BIRTHDATE_PRUEBA1
        
        data1.username=self.USERNAME_PRUEBA1
        data1.email=self.EMAIL_PRUEBA1
        data1.password=self.PASSWORD_PRUEBA1  
        data1.is_admin=self.IS_ADMIN_PRUEBA1
        

        return data1

    
if __name__ == '__main__':
    unittest.main()


