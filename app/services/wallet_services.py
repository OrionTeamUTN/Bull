from app.models import Wallet
from app.repositories.wallet_repository import wallet_repository

repository = wallet_repository()

class walletservices:

    def save(self, wallet: Wallet) -> Wallet:
        return repository.save(wallet)
    
    def find_by_id(self, id_wallet: int):
        return repository.find_by_id(id_wallet)

    def delete(self, wallet: Wallet) -> None:
        repository.delete(wallet)