import unittest
from flask import current_app
from app import create_app, db
from app.models import Coin


class CoinTestCase (unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        #Datos de prueba / "clave" : valor,
        self.coin_data = {
            "id_coin" : 1,
            "coin_name" : "Bitcoin",
            "coin_abbreviation" : "BTC",
       
        }

    def tearDown(self):
        #Esto permite quita los datos de prueba con los que se ejecuto el test
        db.session.remove()
        db.drop_all()

    
    def test_coin(self):
            coin = Coin(**self.coin_data) # ** significa que puede contener varios argumentos

            self.assertTrue(coin.id_coin, self.coin_data["id_coin"])
            self.assertTrue(coin.coin_name, self.coin_data["coin_name"])
            self.assertTrue(coin.coin_abbreviation, self.coin_data["coin_abbreviation"])

if __name__ == "__main__":
     unittest.main() #Ejecuta todos los test que se encuentren en este archivo