from app.models import Coin, Account
from app.repositories.coin_repository import CoinRepository
from app.services.account_services import AccountService
from app.services.format_logs import formatLogs

logging = formatLogs('coinLogger')

class CoinServices:

    def __init__(self) -> None:
        
        self.repository = CoinRepository()
        self.acc_srvc = AccountService()

    # Sólo puede agregar monedas un usuario SUadmin
    def save(self, args: dict, admin_id: int) -> Coin:
        acc_srv = self.acc_srvc.find_by_id(admin_id)
        if isinstance(acc_srv, Account) and acc_srv.id_role == 1:
            coin = Coin()
            for key, value in args.items():
                setattr(coin, key, value) if hasattr (coin, key) else print("Atributo desconocido")
            coin.coin_name = coin.coin_name.capitalize()
            coin.coin_symbol = coin.coin_symbol.upper()
            logging.info("Coin add")
            return self.repository.save(coin)
        else:
            logging.warning("You do not have permission to add a coin")
            return ("No tiene permiso para realizar esta acción")

    # Sólo puede eliminar un usuario SUadmin
    def delete(self, coin_id: int, admin_id: int) -> None:
        acc_srv = self.acc_srvc.find_by_id(admin_id)
        if isinstance(acc_srv, Account) and acc_srv.id_role == 1:
            coin = self.repository.find_by_id(coin_id)
            if isinstance(coin, Coin):
                logging.info("Coin deleted")
                return self.repository.delete(coin)        
        else:
            logging.warning("You do not have permission to remove a coin")
            return ("No tiene permiso para realizar esta acción")
        
    # La función update sólo actualiza si la moneda está o no activa,
    # el resto no tiene sentido actualizarlo.
    # Sólo puede activarla o desactivarla un usuario SUadmin
    def update(self, coin_id: int, admin_id: int) -> Coin:
        acc_srv = self.acc_srvc.find_by_id(admin_id)
        if acc_srv.id_role == 1:
            coin = self.repository.find_by_id(coin_id)
            if isinstance(coin, Coin):
                if coin.is_active == False:
                    setattr(coin, 'is_active', True)
                    logging.info("Currency updated to active")
                else:
                    setattr(coin, 'is_active', False)
                    logging.info("Currency updated to inactive")
                return self.repository.update(coin)
        else:
            logging.warning("You do not have permission to update the status")
            return ("No tiene permiso para realizar esta acción")

    # Función para traer todas las monedas registradas en la DB
    def get_all(self):
        logging.info ("information Coin found ")
        return self.repository.get_all()      

    # Función para buscar una moneda por id
    def find_by_id(self, id: int) -> Coin:
        if id is None or id == 0:
            logging.warning("No coin found with a null id")
            return None
        res = self.repository.find_by_id(id)
        if res != None:
            logging.info("Coin found by id")
            return res
        else:
            logging.warning("Coin not found by id")
            return "Coin not found - 404"
        
    
    # Función para buscar una moneda por nombre
    def find_by_name(self, name: str) -> Coin:
        if name is None or name == '':
            logging.warning("No coin found with a null name")
            return None
        res = self.repository.find_by_name(name.capitalize())
        if res != None: 
            logging.info("Coin found by name")
            return res
        else:
            logging.warning("Coin not found by name")
            return "Coin not found - 404"
        
        
    # Función para buscar una moneda por simbolo
    def find_by_symbol(self, symbol: str) -> Coin:
        if symbol is None or symbol == '':
            logging.warning("No coin found with a null symbol")
            return None
        res = self.repository.find_by_symbol(symbol.upper())
        if res != None:
            logging.info("Coin found by symbol")
            return res
        else:
            logging.warning("Coin not found by symbol")
            return "Coin not found - 404"
        
    
    # Función para buscar todas las monedas activas
    def get_active_coins(self) -> list[Coin]:
        logging.info("Request from all active wallets")
        return self.repository.get_active_coins()
    
    # Función para buscar todas las monedas inactivas
    def get_inactive_coins(self) -> list[Coin]:
        logging.info("Request for all inactive wallets")
        return self.repository.get_inactive_coins()

