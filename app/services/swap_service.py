from app import db
from app.repositories.swap_repository import SwapRepository
from app.models import Swap 

swap_repository = SwapRepository()

class SwapService:

    def save(self, swap: Swap):
        swap_repository.save(swap)

    def get_all(self):
        return swap_repository.get_all()
    
    def find_by_id(self, id_swap: int):
        return swap_repository.find_by_id(id_swap)
    
    def filter_by_wallet_id(self, id_wallet: int):
        return swap_repository.filter_by_wallet_id(id_wallet)