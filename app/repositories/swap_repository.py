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

    # Busca swaps relacionados con una wallet en particular, por su id, ya sea que envió o recibió dinero.
    def filter_by_wallet_id(self, id_wallet: int):
        l_swaps1 = db.session.query(Swap).filter_by(id_wallet_in=id_wallet).all() # busco en las que figure que envie
        l_swaps2 = db.session.query(Swap).filter_by(id_wallet_out=id_wallet).all() # busco en las que figure que recibe
        l_swaps = l_swaps1 + l_swaps2 # combino ambas listas
        if len(l_swaps) > 0: 
            return l_swaps
        else:
            return None
    
    # Busca por fecha de operación
    def find_by_op_date(self, operation_date: datetime):
        swaps = db.session.query(Swap).filter_by(operation_date=operation_date).all()
        return swaps
    
    # Busca por fecha de operación y billetera en particular
    def find_by_op_date_and_wallet(self, operation_date: datetime, id_wallet: int):
        swaps_by_opdate = self.find_by_op_date(operation_date)
        pass