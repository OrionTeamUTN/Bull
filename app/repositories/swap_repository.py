from app.models import Swap 
from app import db 
from datetime import datetime 

class SwapRepository:

    def save(self, swap: Swap):
        """ Guarda un Swap en la BD. """
        db.session.add(swap)
        db.session.commit()
    
    
    def get_all(self) -> list[Swap]:
        """ Retorna una lista de todos los swaps. """
        swaps = db.session.query(Swap).all()
        return swaps

    
    def find_by_id(self, id_swap: int) -> Swap:
        """ Busca un swap por su id. """
        try:
            swap = db.session.query(Swap).filter_by(id_swap=id_swap).one()
            return swap
        except: # Si no existe, devuelve none
            return None

    
    def filter_by_wallet_send(self, id_wallet: int) -> list[Swap]:
        """ Filtra por una wallet en particular, por su id, que haya enviado swaps. """
        l_swaps = db.session.query(Swap).filter_by(id_wallet_send=id_wallet).all() 
        return l_swaps # Si no encuentra ninguno, devuelve una lista vacía

    
    def filter_by_wallet_recv(self, id_wallet: int) -> list[Swap]:
        """ Filtra por una wallet que haya recibido swaps. """
        l_swaps = db.session.query(Swap).filter_by(id_wallet_recv=id_wallet).all()
        return l_swaps
