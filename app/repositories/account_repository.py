from app.models import Account
from app import db
from sqlalchemy.exc import IntegrityError, NoResultFound

class AccounRepository: 
    """Aplicamos responsabilidad única"""
    
    def save(self, account: Account) -> Account:
        try:
            db.session.add(account) 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print("Rollback en repository 1")
        return account
        
    
    def delete(self, user: Account) -> None:
        try:
            db.session.delete(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print("Rollback en repository 2")
        
        
    def find_by_id(self, id: int) -> Account :
        try:
            return db.session.query(Account).filter(Account.id_account == id).one()
        except NoResultFound:
            return None

            
    
    def find_by_dni(self, dni: int):
        try:
            return db.session.query(Account).filter(Account.dni == dni).first()
        except NoResultFound:
            return None
        
    def find_by_username(self, username: str):
        try:
            return db.session.query(Account).filter(Account.username == username).one_or_none()
        except NoResultFound:
            return None
        
    def update(self, account: Account, id: int) -> Account:
        try:
            db.session.add(account)
            db.session.commit()
        except IntegrityError:
            print("Rollback en update")
            db.session.rollback()
        return account
        
        
