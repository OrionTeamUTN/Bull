from app.models import Coin
from app import db


class coin_repository: 
    
    def save(self, coin: Coin) -> Coin:
        db.session.add(coin) 
        db.session.commit()
        return self
    
    def delete(self, coin: Coin) -> None:
        db.session.delete(coin)
        db.session.commit()