import unittest
from . import BaseTestClass as base_t
from app.services.role_services import RoleServices

class RoleTestCase(base_t):

    role_srv = RoleServices()

    # Test para funcionalidad de crear tests
    def test_save(self, admin_id=0):
        
        res_1 = self.role_srv.save(self.role_data_4, admin_id)
        res_2 = self.role_srv.save(self.role_data_4, admin_id)

        self.assertEqual(self.role_data_4["role_name"].capitalize(), res_1.role_name)
        
        self.assertEqual(res_2, None)

    # Test para funcionalidad delete
    def test_delete(self, admin_id=0):
        res = self.role_srv.delete(self.role_3.id_role, admin_id)
        self.assertEqual(res, "Deleted")
        # Le pasamos una cuenta inexistente para probar que arroje el error
        res_2 = self.role_srv.delete(7, admin_id)
        res_3 = self.role_srv.delete(5, 7)
        self.assertEqual(res_2, None)
        self.assertEqual(res_3, 'No tiene permiso para realizar esta acción')

    # Test para funcionalidad update
    def test_update(self, admin_id=0):
        
        res_1 = self.role_srv.update(self.role_3.id_role, self.role_data_5, admin_id)
        self.assertEqual(res_1.role_name, self.role_data_5["role_name"].capitalize())

        res_2 = self.role_srv.update(self.role_2.id_role, self.role_data_5, admin_id)
        self.assertEqual(res_2, None)

        res_3 = self.role_srv.update(self.role_2.id_role, self.role_data_5, 8)
        self.assertEqual(res_3, 'No tiene permiso para realizar esta acción')

        res_4 = self.role_srv.update(9, self.role_data_5, admin_id)
        self.assertEqual(res_4, "No existe el rol")

    # Test para funcionalidad buscar por id de rol
    def test_find_by_id(self):
        res_1 = self.role_srv.find_by_id(1)
        res_2 = self.role_srv.find_by_id(9)

        self.assertEqual(res_1.role_name, self.role_1.role_name)
        self.assertEqual(res_2, "Role not found - 404")

    # Test para funcionalidad buscar por nombre de rol
    def test_role_name(self):
        res_1 = self.role_srv.find_by_role_name('suadmin')
        res_2 = self.role_srv.find_by_role_name('superman')

        self.assertEqual(res_1.role_name, self.role_1.role_name)
        self.assertEqual(res_2, "Role not found - 404")

    # Test para funcionalidad de obtener todos los roles
    def test_get_all_roles(self):
        res = self.role_srv.get_all_roles()
        self.assertEqual(res[0].role_name, self.role_1.role_name)
        self.assertEqual(res[1].role_name, self.role_2.role_name)


if __name__ == '__main__':
    unittest.main()