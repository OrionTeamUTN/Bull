from app import db
from app.repositories.swap_repository import SwapRepository
from app.services.wallet_services import WalletServices
from app.services.coin_services import CoinServices
from app.models import Swap 
from app.services.get_prices import CoinPrices
from datetime import datetime

swap_repository = SwapRepository()
wallet_service = WalletServices()
coin_service = CoinServices()
coin_prices = CoinPrices()

class SwapService:

    def make_swap(self, coin1_symbol: str, coin2_symbol: str, amount_send: float):

        # Verificamos que existan las monedas
        if coin_service.find_by_symbol(coin1_symbol) == "Coin not found - 404":
            print("No existe la Coin de Send")
            return None 
        if coin_service.find_by_symbol(coin2_symbol) == "Coin not found - 404":
            print("No existe la Coin de Recv")
            return None

        # Verificar que esten activas??? Probablemente sí

        # Convertimos el monto enviado al monto que se recibe (mediante USDT)
        amount_send_USDT = coin_prices.crypto_to_stable(coin1_symbol, amount_send, 'USDT') # monto enviado en USDT
        amount_recv = coin_prices.stable_to_crypto(coin2_symbol, 'USDT', amount_send_USDT) # monto recibido

        return amount_recv


    def save(self, swap: Swap):
        """ Guarda un swap en la BD, con procesos de verificación de wallets y montos. """

        # Se verifica que existan las billeteras
        wallet_send = wallet_service.find_by_id(swap.id_wallet_send)
        wallet_recv = wallet_service.find_by_id(swap.id_wallet_recv)
        if wallet_send == None:
            print(f"No existe la WALLET SEND con id={swap.id_wallet_send}")
            return None
        if wallet_recv == None:
            print(f"No existe la WALLET RECV con id={swap.id_wallet_recv}")
            return None

        # Se verifica que el monto del swap no sea mayor al balance 
        # Consumimos el monto del balance de la wallet
        w = wallet_service.withdraw(swap.id_wallet_send, amount=swap.amount_send)
        if isinstance(w, str): # Si devuelve un mensaje str, entonces el balance es insuficiente
            print(w)
            return None 

        # Si todo estuvo ok, calculamos el monto a recibir:
        swap.amount_recv = self.make_swap(wallet_send.coin.coin_symbol, wallet_recv.coin.coin_symbol, swap.amount_send)

        # Guardamos el swap.
        swap_repository.save(swap)
        

    def get_all(self) -> list[Swap]:
        """ Retorna una lista de todos los swaps. """
        return swap_repository.get_all()
    
    
    def find_by_id(self, id_swap: int) -> Swap:
        """ Busca un swap por su id. """
        return swap_repository.find_by_id(id_swap)
    

    def filter_by_wallet_send(self, id_wallet: int) -> list[Swap]:
        """ Filtra por una wallet en particular, por su id, que haya enviado swaps. """
        return swap_repository.filter_by_wallet_send(id_wallet)
    

    def filter_by_wallet_recv(self, id_wallet: int) -> list[Swap]:
        """ Filtra por una wallet que haya recibido swaps. """
        return swap_repository.filter_by_wallet_recv(id_wallet)
    

    def filter_by_wallet(self, id_wallet: int) -> list[Swap]:
        """ Filtra todos los swaps (send y recv) de un wallet en particular. """
        l_swaps_send = self.filter_by_wallet_send(id_wallet)
        l_swaps_recv = self.filter_by_wallet_recv(id_wallet)

        l_swaps = l_swaps_send + l_swaps_recv
        return l_swaps


    def filter_by_op_date(self, l_swaps: list[Swap], op_date: datetime) -> list[Swap]:
        """ Filtra todos los swaps por fecha de operación.
        Recibe una lista de Swaps, y filtra por fecha de esa lista. """
        date_swaps = []
        # Filtramos por fecha de operacion
        for swap in l_swaps:
            day = swap.operation_date.day
            month = swap.operation_date.month
            year = swap.operation_date.year
            if day == op_date.day and month == op_date.month and year == op_date.year: # Se comparan dia, mes y año
                date_swaps.append(swap)
        
        if len(date_swaps)>0:
            return date_swaps 
        else:
            return None
        
    
    def find_by_op_date_and_wallet(self, op_date: datetime, id_wallet: int):
        """ Filtra swaps de un wallet en una fecha en particular. """
        swaps_wallet = self.filter_by_wallet(id_wallet) # Filtramos por wallet id
        swaps_wallet_date = self.filter_by_op_date(swaps_wallet, op_date) # De la anterior, filtramos por fecha.
        return swaps_wallet_date