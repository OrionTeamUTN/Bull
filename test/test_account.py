import unittest
from . import BaseTestClass as base_t
from app.services.account_services import AccountService
from app.services.security import SecurityManager, WerkzeugSecurity

class AccountTestCase(base_t):

    security = SecurityManager(WerkzeugSecurity())
    acc_serv = AccountService()

    # Test para la función que guarda los datos para grabarlos en la DB
    def test_save(self):
        
        res_1 = self.acc_serv.save(self.fake_account_2)
        # Función para recorrer la instancia por cada uno de sus atributos
        # para poder compararlos
        for key in self.fake_account_2.keys():
            # No comparo pass porque uno esta plano y el guardado lo devuelve hasheado
            if key != 'password':
                self.assertEqual(self.fake_account_2[key], getattr(res_1, key))
            else:
            # comparamos la pass de prueba contra la que esta haseada en la DB
                self.assertTrue(self.security.check_password(res_1.password, self.fake_account[key]))
 
    # Test para la función de búsqueda de todas las cuentas
    def test_find_by_id(self):
        
        res_1 = self.acc_serv.find_by_id(1)
        res_2 = self.acc_serv.find_by_id(2)

        self.assertEqual(self.acc_1, res_1)
        self.assertEqual(self.acc_2, res_2)
        self.assertNotEqual(self.fake_account, res_1)
        self.assertNotEqual(self.fake_account, res_2)
    
    # Test para la función de búsqueda por dni
    def test_find_by_dni(self):
        
        res_1 = self.acc_serv.find_by_dni(self.account_1_data["dni"])
        res_2 = self.acc_serv.find_by_dni(self.account_2_data["dni"])
        res_3 = self.acc_serv.find_by_dni(55555555)

        self.assertEqual(self.acc_1, res_1)
        self.assertEqual("No se encontró la cuenta.", res_3)
        self.assertNotEqual(self.fake_account, res_2)
     
    # Test para la función de busqueda por username
    def test_find_by_username(self):

        res_1 = self.acc_serv.find_by_username(self.account_1_data["username"])
        res_2 = self.acc_serv.find_by_username(self.account_2_data["username"])

        self.assertEqual(self.acc_1, res_1)
        self.assertNotEqual(self.fake_account, res_2)

    # Test para la función de buscar una segunda cuenta -- SOLO ADMIN --
    def test_get_other_account_info(self):
        
        res_1 = self.acc_serv.get_other_account_info(self.account_2_data["dni"], self.account_1_data["dni"])
        res_2 = self.acc_serv.get_other_account_info(self.account_1_data["dni"], self.account_2_data["dni"])
        res_3 = self.acc_serv.get_other_account_info(55555555, self.account_1_data["dni"])
        res_4 = self.acc_serv.get_other_account_info(self.account_1_data["dni"], self.account_3_data["dni"])

        self.assertEqual(self.acc_2, res_1)
        self.assertEqual(self.acc_2, res_2)
        self.assertEqual("Acción no permitida para cuentas no administrativas.", res_4)
        self.assertEqual("No se encontró la cuenta.", res_3)

    # Test para la función de verificar la contraseña
    def test_check_auth(self):
        
        res_1 = self.acc_serv.check_auth(self.account_1_data["dni"], self.account_1_data["password"])
        # La contraseña es incorrecta, debe devolver False
        res_2 = self.acc_serv.check_auth(self.account_2_data["dni"], self.account_1_data["password"])

        self.assertTrue(res_1)
        self.assertFalse(res_2)

    # Test para la función de actualizar
    def test_update(self):
        
        res_1 = self.acc_serv.update(self.fake_account, self.acc_2.id_account)
        # Función para recorrer la instancia por cada uno de sus atributos
        # para poder compararlos
        for key in self.fake_account.keys():
            if key != 'password':
                self.assertEqual(self.fake_account[key], getattr(res_1, key))
            else:
            # comparamos la pass de prueba contra la que esta haseada en la DB
                self.assertTrue(self.security.check_password(res_1.password, self.fake_account[key]))
        # Le pasamos una cuenta inexistente para probar que arroje el error
        res_2 = self.acc_serv.update(self.fake_account, 4)
        self.assertEqual(res_2, "No existe la cuenta")
        
    # Test para la función de borrar
    def test_delete(self):
        res = self.acc_serv.delete(self.acc_2.id_account)
        self.assertEqual(res, "Deleted")
        # Le pasamos una cuenta inexistente para probar que arroje el error
        res_2 = self.acc_serv.delete(4)
        self.assertEqual(res_2, 'Error to try delete')

if __name__ == '__main__':
    unittest.main()