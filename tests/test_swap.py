import unittest
from flask import current_app
from app import create_app

from app.models import Swap
from datetime import datetime


# Datos de prueba
id_swap = 1
operation_date = datetime(2014, 5, 17)
amount_in = 400
amount_out = 60
id_wallet_in = 1
id_wallet_out = 2

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_swap(self):
        swap = Swap()
        swap.id_swap = id_swap
        swap.operation_date = operation_date
        swap.amount_in = amount_in
        swap.amount_out = amount_out
        swap.id_wallet_in = id_wallet_in
        swap.id_wallet_out = id_wallet_out
        self.assertTrue(swap.id_swap, id_swap)
        self.assertTrue(swap.operation_date, operation_date)
        self.assertTrue(swap.amount_in, amount_in)
        self.assertTrue(swap.amount_out, amount_out)
        self.assertTrue(swap.id_wallet_in, id_wallet_in)
        self.assertTrue(swap.id_wallet_out, id_wallet_out)

if __name__ == "__main__":
    unittest.main()