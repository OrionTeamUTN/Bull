from app.models import Coin
from app import db
from sqlalchemy.exc import IntegrityError, NoResultFound

class CoinRepository: 
    
    def save(self, coin: Coin) -> Coin:
        try:
            db.session.add(coin) 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return coin
    
    def update(self, coin: Coin) -> Coin:
        try:
            db.session.add(coin) 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return coin
    
    def delete(self, coin: Coin) -> None:   
        try:
            db.session.delete(coin) 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return ("Success")
    
    def get_all(self) -> list[Coin]:
        return db.session.query(Coin).all()
    
    # Consulta para buscar por id
    def find_by_id(self, id: int) -> Coin:
        try:
            return db.session.query(Coin).filter(Coin.id_coin == id).one()
        except NoResultFound:
            return None
        
    # Consulta para buscar por nombre
    def find_by_name(self, name: str) -> Coin:
        try:
            return db.session.query(Coin).filter(Coin.coin_name == name).one()
        except NoResultFound:
            return None

    # Consulta para buscar por simbolo de cripto
    def find_by_symbol(self, symbol: str) -> Coin:
        try:
            return db.session.query(Coin).filter(Coin.coin_symbol == symbol).one()
        except NoResultFound:
            return None
        
    # Consulta para buscar por criptos activas
    def get_active_coins(self) -> Coin:
        return db.session.query(Coin).filter(Coin.is_active == True).all()
    
    # Consulta para buscar por criptos inactivas
    def get_inactive_coins(self) -> Coin:
        return db.session.query(Coin).filter(Coin.is_active == False).all()
        
