import unittest
from . import BaseTestClass as base_t

from app.models import Swap, Wallet
from app.services.swap_service import SwapService
from datetime import datetime

# Nota: en el SetUp de la clase base_t, se crean dos swaps
    # El primero, wallet(id=4) envía a wallet(id=5)
    # El segundo, wallet(id=5) envía a wallet(id=4)
    # Esas dos wallets con coins activas


# Servicios de Swap
swap_service = SwapService()

class SwapTestCase(base_t):

    """ Test del objeto swap """
    def test_swap_as_object(self):
        swap = Swap(**self.swap_data_1)
        self.assertIsInstance(swap, Swap)
        self.assertIsNone(swap.id_swap)
        self.assertEqual(swap.operation_date, self.swap_data_1["operation_date"])
        self.assertEqual(swap.amount_send, self.swap_data_1["amount_send"])
        self.assertEqual(swap.id_wallet_send, self.swap_data_1["id_wallet_send"])
        self.assertEqual(swap.id_wallet_recv, self.swap_data_1["id_wallet_recv"])
        self.assertIsNone(swap.amount_recv) # Aún no se ha calculado el monto recibido por lo que debe ser None
        # Testeamos también los relationship, en este punto debe retornar None ya que solo se instancia un objeto Swap y no está guardado en la BD.
        self.assertIsNone(swap.wallet_send)
        self.assertIsNone(swap.wallet_recv)

    """ Test de comprobación de balance de la wallet send antes y despúes del swap """
    def test_balance_before_and_after_swap(self):
        # Se realizará un swap de wallet 4 a 5
        # Chequeamos el balance de la wallet 4 antes y después del swap
        self.assertEqual(self.wall_4.balance, 500)
        swap = swap_service.save(self.swap_data_1)
        self.assertEqual(self.wall_4.balance, 400)

        # Nota: No veo recomendable testear el balance de la wallet que recibe después del swap, 
        # ya que este variará según el valor de la crypto a la hora de hacer el swap

    """ Test de los atributos del tipo relationship (Wallet) de Swap """
    def test_swap_relationship_to_wallets(self):
        # Como ya hemos creado dos swaps en el SetUp base, ahora sí deberían existir las instancias de las relaciones
        self.assertIsInstance(self.swap_1.wallet_send, Wallet)
        self.assertIsInstance(self.swap_1.wallet_recv, Wallet)

        self.assertIsInstance(self.swap_2.wallet_send, Wallet)
        self.assertIsInstance(self.swap_2.wallet_recv, Wallet)

    """ Test de swap con wallet_send inexistente """
    def test_unexisting_wallet_send(self):
        self.swap_data_1['id_wallet_send'] = 8 # damos un id de wallet sender que no exista
        swap = swap_service.save(self.swap_data_1) 
        self.assertIsNone(swap)

    """ Test de swap con monto enviado invalido, superior al balance de la wallet """
    def test_invalid_amount_send(self):
        self.swap_data_1['amount_send'] = 1000
        swap = swap_service.save(self.swap_data_1)
        self.assertIsNone(swap)

    """ Test de obtener una lista de todos los registros swaps """ 
    def test_get_all_swaps(self):
        l_swaps = swap_service.get_all()
        self.assertIsInstance(l_swaps, list)
        self.assertEqual(len(l_swaps), 2)

    """ Test de buscar un swap por su id """
    def test_find_by_id(self):
        finded_swap1 = swap_service.find_by_id(1)
        finded_swap2 = swap_service.find_by_id(2)
        finded_swap3 = swap_service.find_by_id(3)
        self.assertEqual(finded_swap1.id_swap, 1)
        self.assertEqual(finded_swap2.id_swap, 2)
        self.assertIsNone(finded_swap3) # el swap con id=3 no debería existir, por lo que debe ser None

    """ Test de filtrar registros de swaps por wallets que hayan envíado o recibido dinero """ 
    def test_filter_by_wallet_send_and_recv(self):
        # Creamos más swaps, cambiando algunos datos
        self.swap_data_1["amount_send"] = 50
        self.swap_data_2["amount_send"] = 320
        swap_service.save(self.swap_data_1)
        swap_service.save(self.swap_data_2)

        # Filtramos swaps por wallets que enviaron dinero
        swaps_sends_from_wallet_4 = swap_service.filter_by_wallet_send(4)
        swaps_sends_from_wallet_5 = swap_service.filter_by_wallet_send(5)
        swaps_sends_from_wallet_1 = swap_service.filter_by_wallet_send(1)

        # Filtramos swaps por wallets que recibieron dinero
        swaps_recvs_from_wallet_4 = swap_service.filter_by_wallet_recv(4)
        swaps_recvs_from_wallet_5 = swap_service.filter_by_wallet_recv(5)
        swaps_recvs_from_wallet_1 = swap_service.filter_by_wallet_recv(1)

        self.assertEqual(len(swaps_sends_from_wallet_4), 2)
        self.assertEqual(len(swaps_sends_from_wallet_5), 2)
        self.assertIsNone(swaps_sends_from_wallet_1) # La wallet 1 no tiene swaps

        self.assertEqual(len(swaps_recvs_from_wallet_4), 2)
        self.assertEqual(len(swaps_recvs_from_wallet_5), 2)
        self.assertIsNone(swaps_recvs_from_wallet_1) 

    """ Test que filtra swaps por fecha de operación """
    def test_filter_by_op_date(self):
        today_date = datetime.today()
        date_1 = datetime(2024, 5, 17)
        date_2 = datetime(2024, 7, 9) # fecha en la que no habrá swaps

        # Creamos un swap más con fecha de operación date_1, modificando también el monto enviado
        self.swap_data_1["operation_date"] = date_1
        self.swap_data_1["amount_send"] = 80
        swap_service.save(self.swap_data_1)

        all_swaps = swap_service.get_all()
        today_swaps = swap_service.filter_by_op_date(all_swaps, today_date)
        date_1_swaps = swap_service.filter_by_op_date(all_swaps, date_1)
        date_2_swaps = swap_service.filter_by_op_date(all_swaps, date_2)

        self.assertEqual(len(today_swaps),1)
        self.assertEqual(len(date_1_swaps),2)
        self.assertIsNone(date_2_swaps)

    """ Test de filtración de swaps de una wallet en una fecha en específico """
    def test_filter_by_wallet_at_op_date(self):
        today_date = datetime.today()
        date_1 = datetime(2024, 5, 17)
        date_2 = datetime(2024, 7, 9)

        swaps_from_wallet_4_today = swap_service.filter_by_wallet_at_op_date(today_date, 4) # swaps de la wallet 4 de hoy
        swaps_from_wallet_5_today = swap_service.filter_by_wallet_at_op_date(today_date, 5) # swaps de la wallet 5 de hoy
        swaps_from_wallet_4_at_date_1 = swap_service.filter_by_wallet_at_op_date(date_1, 4) # swaps de la wallet 4 de la fecha 2024-5-17
        swaps_from_wallet_4_at_date_2 = swap_service.filter_by_wallet_at_op_date(date_2, 4) # swaps de la wallet 4 de la fecha 2024-7-9, los cuales no existen

        self.assertEqual(len(swaps_from_wallet_4_today), 1)
        self.assertEqual(len(swaps_from_wallet_5_today), 1)
        self.assertEqual(len(swaps_from_wallet_4_at_date_1),1)
        self.assertIsNone(swaps_from_wallet_4_at_date_2)

if __name__ == "__main__":
    unittest.main()