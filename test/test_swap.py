import unittest
from flask import current_app
from app import create_app

from app.models import Swap
from datetime import datetime

class SwapTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
        # Datos de prueba
        self.ID_SWAP = 1
        self.OPERATION_DATE = datetime.utcnow()
        self.AMOUNT_IN = 400
        self.AMOUNT_OUT = 60
        self.ID_WALLET_IN = 1
        self.ID_WALLET_OUT = 2

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_swap(self):
        swap = Swap()
        swap.id_swap = self.ID_SWAP
        swap.operation_date = self.OPERATION_DATE
        swap.amount_in = self.AMOUNT_IN
        swap.amount_out = self.AMOUNT_OUT
        swap.id_wallet_in = self.ID_WALLET_IN
        swap.id_wallet_out = self.ID_WALLET_OUT
        self.assertTrue(swap.id_swap, self.ID_SWAP)
        self.assertTrue(swap.operation_date, self.OPERATION_DATE)
        self.assertTrue(swap.amount_in, self.AMOUNT_IN)
        self.assertTrue(swap.amount_out, self.AMOUNT_OUT)
        self.assertTrue(swap.id_wallet_in, self.ID_WALLET_IN)
        self.assertTrue(swap.id_wallet_out, self.ID_WALLET_OUT)

if __name__ == "__main__":
    unittest.main()