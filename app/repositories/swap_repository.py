from app.models import Swap 
from app import db 
from datetime import datetime 

class SwapRepository:

    def save(self, swap: Swap):
        db.session.add(swap)
        db.session.commit()
    
    def get_all(self):
        swaps = db.session.query(Swap).all()
        return swaps

    # Busca un swap por su id
    def find_by_id(self, id_swap: int):
        try:
            swap = db.session.query(Swap).filter_by(id_swap=id_swap).one()
            return swap
        except: # Si no existe, devuelve none
            return None

    # Buscar por una wallet en particular, por su id, que haya enviado swaps
    def filter_by_wallet_send(self, id_wallet: int):
        l_swaps = db.session.query(Swap).filter_by(id_wallet_send=id_wallet).all()
        if len(l_swaps)>0:
            return l_swaps
        else:
            return None

    # Filtra por una wallet que haya recibido swaps
    def filter_by_wallet_recv(self, id_wallet: int):
        l_swaps = db.session.query(Swap).filter_by(id_wallet_recv=id_wallet).all()
        if len(l_swaps)>0:
            return l_swaps
        else:
            return None

