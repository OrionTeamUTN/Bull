from app.models import Swap 
from app import db 
from datetime import datetime 

class SwapRepository:

    def save(self, swap: Swap) -> Swap:
        """ Guarda un Swap en la BD. """
        db.session.add(swap)
        db.session.commit()
        return swap
    
    def get_all(self) -> list[Swap]:
        """ Retorna una lista de todos los swaps, ordenamos por fecha. """
        swaps = db.session.query(Swap).order_by(Swap.operation_date).all()
        return swaps

    
    def find_by_id(self, id_swap: int) -> Swap:
        """ Busca un swap por su id. """
        try:
            swap = db.session.query(Swap).filter(Swap.id_swap == id_swap).order_by(Swap.operation_date).one()
            return swap
        except: # Si no existe, devuelve none
            return None

    
    def filter_by_wallet_send(self, id_wallet: int) -> list[Swap]:
        """ Filtra por una wallet en particular, por su id, que haya enviado swaps. """
        return db.session.query(Swap).filter(Swap.id_wallet_send == id_wallet).order_by(Swap.operation_date).all() 
        

    
    def filter_by_wallet_recv(self, id_wallet: int) -> list[Swap]:
        """ Filtra por una wallet que haya recibido swaps. """
        return db.session.query(Swap).filter(Swap.id_wallet_recv == id_wallet).order_by(Swap.operation_date).all()
