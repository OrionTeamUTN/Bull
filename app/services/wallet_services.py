from app.models import Wallet
from app.repositories.wallet_repository import wallet_repository

repository = wallet_repository()

class walletservices:

    def save(self, wallet: Wallet) -> Wallet:
        return repository.save(wallet)

    def delete(self, wallet: Wallet) -> None:
        repository.delete(wallet)