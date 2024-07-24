from app import db
from app.repositories.swap_repository import SwapRepository
from app.services.wallet_services import WalletServices
from app.services.coin_services import CoinServices
from app.models import Swap 
from app.services.get_prices import CoinPrices
from datetime import datetime


class SwapService:

    def __init__(self):
        self.swap_repository = SwapRepository()
        self.wallet_service = WalletServices()
        self.coin_service = CoinServices()
        self.coin_prices = CoinPrices()

    def make_swap(self, coin1_symbol: str, coin2_symbol: str, amount_send: float):

        coin1 = self.coin_service.find_by_symbol(coin1_symbol)
        coin2 = self.coin_service.find_by_symbol(coin2_symbol)
        # Verificamos que existan las monedas
        if coin1 == "Coin not found - 404":
            print("No existe la Coin Send")
            return None 
        if coin2 == "Coin not found - 404":
            print("No existe la Coin Recv")
            return None

        # Verificamos que las monedas estén activas
        if not coin1.is_active:
            print("Coin Send no está activa")
            return None
        if not coin2.is_active:
            print("Coin Recv no está activa")
            return None        

        # Convertimos el monto enviado al monto que se recibe (mediante USDT)
        amount_send_USDT = self.coin_prices.crypto_to_stable(coin1_symbol, amount_send, 'USDT') # monto enviado en USDT
        amount_recv = self.coin_prices.stable_to_crypto(coin2_symbol, 'USDT', amount_send_USDT) # monto recibido

        return amount_recv


    def save(self, args: dict):
        """ Guarda un swap en la BD, con procesos de verificación de wallets y montos. """
        swap = Swap(**args)

        # Se verifica que existan las billeteras
        wallet_send = self.wallet_service.find_by_id(swap.id_wallet_send)
        wallet_recv = self.wallet_service.find_by_id(swap.id_wallet_recv)
        if wallet_send == None:
            print(f"No existe la WALLET SEND con id={swap.id_wallet_send}")
            return None
        if wallet_recv == None:
            print(f"No existe la WALLET RECV con id={swap.id_wallet_recv}")
            return None

        # Se verifica que el monto del swap no sea mayor al balance 
        # Consumimos el monto del balance de la wallet
        w = self.wallet_service.withdraw(swap.id_wallet_send, amount=swap.amount_send)
        if isinstance(w, str): # Si devuelve un mensaje str, entonces el balance es insuficiente
            print(w)
            return None 

        # Si todo estuvo ok, calculamos el monto a recibir:
        swap.amount_recv = self.make_swap(wallet_send.coin.coin_symbol, wallet_recv.coin.coin_symbol, swap.amount_send)

        # Acreditamos el nuevo balance a la billetera que recibe.
        new_balance = wallet_recv.balance + swap.amount_recv 
        self.wallet_service.update(wallet_recv.id_wallet, new_balance)

        # Guardamos el swap.
        return self.swap_repository.save(swap)

        

    def get_all(self) -> list[Swap]:
        """ Retorna una lista de todos los swaps. """
        return self.swap_repository.get_all()
    
    
    def find_by_id(self, id_swap: int) -> Swap:
        """ Busca un swap por su id. """
        return self.swap_repository.find_by_id(id_swap)
    

    def filter_by_wallet_send(self, id_wallet: int) -> list[Swap]:
        """ Filtra por una wallet en particular, por su id, que haya enviado swaps. """
        l_swaps = self.swap_repository.filter_by_wallet_send(id_wallet)
        return l_swaps if len(l_swaps)>0 else None
    

    def filter_by_wallet_recv(self, id_wallet: int) -> list[Swap]:
        """ Filtra por una wallet que haya recibido swaps. """
        l_swaps = self.swap_repository.filter_by_wallet_recv(id_wallet)
        return l_swaps if len(l_swaps)>0 else None
    

    def filter_by_wallet(self, id_wallet: int) -> list[Swap]:
        """ Filtra todos los swaps (send y recv) de un wallet en particular. """
        l_swaps_send = self.filter_by_wallet_send(id_wallet)
        l_swaps_recv = self.filter_by_wallet_recv(id_wallet)

        l_swaps = l_swaps_send + l_swaps_recv
        return l_swaps if len(l_swaps)>0 else None


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
        
        return date_swaps if len(date_swaps)>0 else None
        
    
    def filter_by_wallet_at_op_date(self, op_date: datetime, id_wallet: int):
        """ Filtra swaps de un wallet en una fecha en particular. """
        swaps_wallet = self.filter_by_wallet(id_wallet) # Filtramos por wallet id
        if swaps_wallet: # Si existen swaps de esa billetera, entonces filtramos por fecha
            swaps_wallet_at_date = self.filter_by_op_date(swaps_wallet, op_date)
            res = swaps_wallet_at_date # Puede ser una lista o bien None si es que no encontró swaps en esa fecha
        else:
            res = None
        return res