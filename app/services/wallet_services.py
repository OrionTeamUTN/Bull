from app.models import Wallet
from app.repositories.wallet_repository import WalletRepository
from app.services.format_logs import formatLogs
from app.services.account_services import AccountService
from app.services.coin_services import CoinServices

logging = formatLogs('walletLogger')



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
            logging.warning("account not found to save wallet")
            return None
        if coin_srv is None or isinstance(coin_srv, str):
            logging.warning("Coin not found to save wallet")
            return None
        wallet.id_owner_account = acc_id
        wallet.id_wallet_coin = coin_id
        logging.info("wallet saved")
        return self.repository.save(wallet)
    
    # Solo se debe poder actualizar el balance
    def update(self, wallet_id: int, balance: int) -> Wallet:
        wallet = self.find_by_id(wallet_id)
        if wallet is None:
            logging.warning("No se puede actualizar")
            return None
        if balance < 0:
            logging.warning("EL balance no puede ser negativo")
            return "Balance cannot be negative"
        else:
            wallet.balance = balance
            logging.info("Billetera actualizada con exito")
            return self.repository.update(wallet)

    def delete(self, wallet_id: int) -> None:
        wallet = self.find_by_id(wallet_id)
        if wallet is None:
            logging.warning("Could not delete wallet ")
            return None
        else:
            logging.info("Wallet deleted")
            return self.repository.delete(wallet)

    def get_all(self) -> list[Wallet]:
        logging.info("Billeteras traidas con exito")
        return self.repository.get_all()

    def find_by_id(self, wallet_id: int) -> Wallet:
        if wallet_id == None or wallet_id == 0:
            logging.warning("wallet not found by id")
            return None
        else:
            logging.info("wallet found by id")
            return self.repository.find_by_id(wallet_id)

    def find_by_coin_name(self, coin_name: str) -> Wallet:
        coin_srv = self.coin_srvc.find_by_name(coin_name)
        if coin_srv is None or isinstance(coin_srv, str):
            logging.warning("wallet not found by name")
            return None
        else:
            logging.info("wallet found by name")
            return self.repository.find_by_coin_name(coin_srv.id_coin)

    def find_by_coin_symbol(self, coin_symbol: str) -> Wallet:
        coin_srv = self.coin_srvc.find_by_symbol(coin_symbol.upper())
        if coin_srv is None or isinstance(coin_srv, str):
            logging.warning("wallet not found by symbol")
            return None
        else:
            logging.info("wallet found by symbol")
            return self.repository.find_by_coin_symbol(coin_srv.id_coin)

    def check_balance(self, wallet_id: int) -> bool:
        wallet = self.find_by_id(wallet_id)
        if wallet is None:
            logging.warning("Not have balance")
            return None
        else:
            logging.info("your balance")
            return wallet.balance > 0
        
    # Función para retirar balance de billetera
    def withdraw(self, wallet_id: int, amount: int) -> Wallet:
        wallet = self.find_by_id(wallet_id)
        if wallet is None:
            logging.warning("Not have amount")
            return None
        if amount < 0:
            logging.warning("Amount cannot be negative")
            return "Amount cannot be negative"
        if wallet.balance < amount:
            logging.warning("Insufficient balance")
            return "Insufficient balance"
        wallet.balance -= amount
        logging.info("retiro exitoso")
        return self.repository.update(wallet)

    # Listar todas las billeteras existentes relacionadas a un usuario
    # que tengan balance positivo
    def find_by_positive_balance(self) -> list[Wallet]:
        logging.info("Wallet whit balance positive found")
        return self.repository.find_by_positive_balance()

    # Listar todas las billeteras existentes relacionadas a un usuario
    # que tengan balance cero
    def find_by_zero_balance(self) -> list[Wallet]:
        logging.info("Wallet whit balance zero found")
        return self.repository.find_by_zero_balance()