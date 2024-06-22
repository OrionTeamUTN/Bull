from app.models import Coin, Account
from app.repositories.coin_repository import CoinRepository
from app.services.account_services import AccountService

class CoinServices:

    def __init__(self) -> None:
        
        self.repository = CoinRepository()
        self.acc_srvc = AccountService()

    # Sólo puede agregar monedas un usuario admin
    def save(self, args: dict, admin_id: int) -> Coin:
        acc_srv = self.acc_srvc.find_by_id(admin_id)
        if isinstance(acc_srv, Account) and acc_srv.is_admin == True:
            coin = Coin()
            for key, value in args.items():
                setattr(coin, key, value) if hasattr (coin, key) else print("Atributo desconocido")
            coin.coin_name = coin.coin_name.capitalize()
            coin.coin_symbol = coin.coin_symbol.upper()
            return self.repository.save(coin)
        else:
            return ("No tiene permiso para realizar esta acción")

    # Sólo puede eliminar un usuario admin
    def delete(self, coin_id: int, admin_id: int) -> None:
        acc_srv = self.acc_srvc.find_by_id(admin_id)
        if isinstance(acc_srv, Account) and acc_srv.is_admin == True:
            coin = self.repository.find_by_id(coin_id)
            if isinstance(coin, Coin):
                return self.repository.delete(coin)        
        else:
            return ("No tiene permiso para realizar esta acción")
        
    # La función update sólo actualiza si la moneda está o no activa,
    # el resto no tiene sentido actualizarlo.
    # Sólo puede activarla o desactivarla un usuario admin
    def update(self, coin_id: int, admin_id: int) -> Coin:
        acc_srv = self.acc_srvc.find_by_id(admin_id)
        if acc_srv.is_admin == True:
            coin = self.repository.find_by_id(coin_id)
            if isinstance(coin, Coin):
                if coin.is_active == False:
                    setattr(coin, 'is_active', True)
                else:
                    setattr(coin, 'is_active', False)
                return self.repository.update(coin)
        else:
            return ("No tiene permiso para realizar esta acción")

    # Función para traer todas las monedas registradas en la DB
    def get_all(self):
        return self.repository.get_all()      

    # Función para buscar una moneda por id
    def find_by_id(self, id: int) -> Coin:
        if id is None or id == 0:
            return None
        res = self.repository.find_by_id(id)
        return res if res != None else "Coin not found - 404"
    
    # Función para buscar una moneda por nombre
    def find_by_name(self, name: str) -> Coin:
        if name is None or name == '':
            return None
        res = self.repository.find_by_name(name.capitalize())
        return res if res != None else "Coin not found - 404"
        
    # Función para buscar una moneda por simbolo
    def find_by_symbol(self, symbol: str) -> Coin:
        if symbol is None or symbol == '':
            return None
        res = self.repository.find_by_symbol(symbol.upper())
        return res if res != None else "Coin not found - 404"
    
    # Función para buscar todas las monedas activas
    def get_active_coins(self) -> list[Coin]:
        return self.repository.get_active_coins()
    
    # Función para buscar todas las monedas inactivas
    def get_inactive_coins(self) -> list[Coin]:
        return self.repository.get_inactive_coins()

