from app.models import Coin
from app.repositories.coin_repository import coin_repository

repository = coin_repository()

class coinservices:

    def save(self, coin: Coin) -> Coin:
        return repository.save(coin)

    def delete(self, coin: Coin) -> None:
        repository.delete(coin)