from app.models import Wallet
from app.repositories.wallet_repository import WalletRepository
from app.services.account_services import AccountService
from app.services.coin_services import CoinServices


class WalletServices:

    def __init__(self) -> None:
        self.repository = WalletRepository()
        self.acc_srvc = AccountService()
        self.coin_srvc = CoinServices()

    def save(self, acc_id: int, coin_id: int) -> Wallet:
        wallet = Wallet()
        acc_srv = self.acc_srvc.find_by_id(acc_id)
        coin_srv = self.coin_srvc.find_by_id(coin_id)
        if acc_srv is None or isinstance(acc_srv, str):
            return None
        if coin_srv is None or isinstance(coin_srv, str):
            return None
        wallet.id_owner_account = acc_id
        wallet.id_wallet_coin = coin_id
        return self.repository.save(wallet)
    
    # Solo se debe poder actualizar el balance
    def update(self, wallet_id: int, balance: int) -> Wallet:
        wallet = self.find_by_id(wallet_id)
        if wallet is None:
            return None
        if balance < 0:
            return "Balance cannot be negative"
        else:
            wallet.balance = balance
            return self.repository.update(wallet)

    def delete(self, wallet_id: int) -> None:
        wallet = self.find_by_id(wallet_id)
        if wallet is None:
            return None
        else:
            return self.repository.delete(wallet)

    def get_all(self) -> list[Wallet]:
        return self.repository.get_all()

    def find_by_id(self, wallet_id: int) -> Wallet:
        if wallet_id == None or wallet_id == 0:
            return None
        else:
            return self.repository.find_by_id(wallet_id)

    def find_by_coin_name(self, coin_name: str) -> Wallet:
        coin_srv = self.coin_srvc.find_by_name(coin_name)
        if coin_srv is None or isinstance(coin_srv, str):
            return None
        else:
            return self.repository.find_by_coin_name(coin_srv.id_coin)

    def find_by_coin_symbol(self, coin_symbol: str) -> Wallet:
        coin_srv = self.coin_srvc.find_by_symbol(coin_symbol.upper())
        if coin_srv is None or isinstance(coin_srv, str):
            return None
        else:
            return self.repository.find_by_coin_symbol(coin_srv.id_coin)

    def check_balance(self, wallet_id: int) -> bool:
        wallet = self.find_by_id(wallet_id)
        if wallet is None:
            return None
        else:
            return wallet.balance > 0
        
    # Función para retirar balance de billetera
    def withdraw(self, wallet_id: int, amount: int) -> Wallet:
        wallet = self.find_by_id(wallet_id)
        if wallet is None:
            return None
        if amount < 0:
            return "Amount cannot be negative"
        if wallet.balance < amount:
            return "Insufficient balance"
        wallet.balance -= amount
        return self.repository.update(wallet)

    # Listar todas las billeteras existentes relacionadas a un usuario
    # que tengan balance positivo
    def find_by_positive_balance(self) -> list[Wallet]:
        return self.repository.find_by_positive_balance()

    # Listar todas las billeteras existentes relacionadas a un usuario
    # que tengan balance cero
    def find_by_zero_balance(self) -> list[Wallet]:
        return self.repository.find_by_zero_balance()