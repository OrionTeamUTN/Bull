from app import db
from app.repositories.swap_repository import SwapRepository
from app.services.wallet_services import walletservices
from app.models import Swap 
from datetime import datetime

swap_repository = SwapRepository()
wallet_service = walletservices()


class SwapService:

    def save(self, swap: Swap):
        
        # Se verifica que existan las billeteras
        wallet_send = wallet_service.find_by_id(swap.id_wallet_send)
        wallet_recv = wallet_service.find_by_id(swap.id_wallet_recv)
        if wallet_send == None:
            print(f"No existe la billetera enviadora con id={swap.id_wallet_send}")
            return None
        if wallet_recv == None:
            print(f"No existe la billetera receptora con id={swap.id_wallet_recv}")
            return None

        # Se verifica que el monto del swap no sea mayor al balance 
        if wallet_send.balance < swap.amount_send: 
            print(f"El monto {swap.amount_send} envíado es superior al balance {wallet_send.balance}")
            return None 

        # Si todo está ok, entonces guardamos el swap.
        swap_repository.save(swap)

        # RECORDATORIO: Restar al balance a la wallet con el amount_send... ¿Pero eso hacerlo aca, o en el servicio wallet?.
        # Requiere un update del balance de esa wallet.

    def get_all(self):
        return swap_repository.get_all()
    
    def find_by_id(self, id_swap: int):
        return swap_repository.find_by_id(id_swap)
    
    def filter_by_wallet_send(self, id_wallet: int):
        return swap_repository.filter_by_wallet_send(id_wallet)
    
    def filter_by_wallet_recv(self, id_wallet: int):
        return swap_repository.filter_by_wallet_recv(id_wallet)
    
    def filter_by_op_date(self, op_date: datetime):
        all_swaps = self.get_all() # nos traemos todos los swaps de la BD
        date_swaps = []
        # Filtramos por fecha de operacion
        for swap in all_swaps:
            day = swap.operation_date.day
            month = swap.operation_date.month
            year = swap.operation_date.year
            if day == op_date.day and month == op_date.month and year == op_date.year: # Se comparan dia, mes y año
                date_swaps.append(swap)
        
        if len(date_swaps)>0:
            return date_swaps 
        else:
            return None
        
    # Busca por fecha de operación y billetera en particular
    def find_by_op_date_and_wallet(self, operation_date: datetime, id_wallet: int):
        swaps_by_opdate = self.find_by_op_date(operation_date)
        pass