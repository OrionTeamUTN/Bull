from app.models import Wallet
from app import db
from sqlalchemy.exc import IntegrityError, NoResultFound

class WalletRepository: 
    
    def save(self, wallet: Wallet) -> Wallet:
        try:
            db.session.add(wallet) 
            db.session.commit()
            return wallet
        except IntegrityError:
            db.session.rollback()
            print("Rollback en repository")
    
    def update(self, wallet: Wallet) -> Wallet:
        try:
            db.session.add(wallet) 
            db.session.commit()
            return wallet
        except IntegrityError:
            db.session.rollback()
            print("Rollback en repository")
    
    def delete(self, wallet: Wallet) -> None:
        try:
            db.session.delete(wallet)
            db.session.commit()
            return "Deleted"
        except IntegrityError:
            db.session.rollback()
            print("Rollback en repository")
            return "Rollback"

    def get_all(self) -> list[Wallet]:
        return db.session.query(Wallet).all()

    def find_by_id(self, wallet_id: int) -> Wallet:
        try:
            return db.session.query(Wallet).filter(Wallet.id_wallet == wallet_id).one()
        except NoResultFound:
            return None
        
    def find_by_coin_name(self, coin_id: int) -> Wallet:
        try:
            return db.session.query(Wallet).filter(Wallet.id_wallet_coin == coin_id).one()
        except NoResultFound:
            return None
        
    def find_by_coin_symbol(self, coin_id: int) -> Wallet:
        try:
            return db.session.query(Wallet).filter(Wallet.id_wallet_coin == coin_id).one()
        except NoResultFound:
            return None
        
    def find_by_positive_balance(self) -> list[Wallet]:
        try:
            return db.session.query(Wallet).filter(Wallet.balance > 0).all()
        except NoResultFound:
            return None
        
    def find_by_zero_balance(self) -> list[Wallet]:
        try:
            return db.session.query(Wallet).filter(Wallet.balance == 0).all()
        except NoResultFound:
            return None