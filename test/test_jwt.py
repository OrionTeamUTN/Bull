import unittest
from app.services import JWTSecurity, PyJWT
from . import BaseTestClass as base_t

jwt_security = JWTSecurity(PyJWT())

class TestJWTSecurity(base_t):

    def test_generate_token(self):
        token = jwt_security.generate_token(self.acc_1)
        self.assertIsInstance(token, str)
    
    def test_verify_token(self):
        token = jwt_security.generate_token(self.acc_1)
        payload = jwt_security.verify_token(token)
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload['username'], self.acc_1.username)
        self.assertEqual(payload['id_role'], self.acc_1.id_role)

if __name__ == '__main__':
    unittest.main()
    

