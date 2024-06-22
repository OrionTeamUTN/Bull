from app.models import Wallet
from app import db


class wallet_repository: 
    
    def save(self, wallet: Wallet) -> Wallet:
        db.session.add(wallet) 
        db.session.commit()
        return self
    
    def find_by_id(self, id_wallet: int) -> Wallet:
        if id_wallet > 0:
            wallet = db.session.query(Wallet).filter(Wallet.id_wallet==id_wallet).first()
            return wallet
        else:
            return None

    def delete(self, wallet: Wallet) -> None:
        db.session.delete(wallet)
        db.session.commit()