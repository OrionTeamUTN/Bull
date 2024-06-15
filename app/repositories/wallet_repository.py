from app.models import Wallet
from app import db


class wallet_repository: 
    
    def save(self, wallet: Wallet) -> Wallet:
        db.session.add(wallet) 
        db.session.commit()
        return self
    
    def delete(self, wallet: Wallet) -> None:
        db.session.delete(wallet)
        db.session.commit()