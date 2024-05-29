from app.models import Account
from app import db


class Accounrepository: 
    """Aplicamos responsabilidad única"""
    
    def save(self, account: Account) -> Account:
        db.session.add(account) 
        db.session.commit()
        return self
    
    def delete(self, user: Account) -> None:
        db.session.delete(user)
        db.session.commit()
        
    def find(self, id: int) -> Account :
        if id is None or id == 0:
            return None
        try:
            return db.session.query(Account).filter(Account.id_account == id).one()
        except:
            return None
    
    def find_by_dni(self, dni: int):
        return db.session.query(Account).filter(Account.dni == dni).first()

    def find_by_username(self, username: str):
        return db.session.query(Account).filter(Account.username == username).one_or_none()

    
    def update(self, user: Account, id: int) -> Account:
        entity = self.find(id)
        entity.username = user.username
        entity.email = user.email
        db.session.add(entity)
        db.session.commit()
        return entity
    
            
    def get_other_account_info(self, otra_cuenta_dni, admin_dni):
        #metodo encargado de verificar si el usuario que pide la cuenta es admin
        #para poder utilizar este metodo el admin debe ingresar su dni tambien, para verificar que es admin 
        admin_account = self.find_by_dni(admin_dni)
        if admin_account and admin_account.is_admin == True :
            try: 
                #si es admin, traera la informacion de la cuenta que el admin desee conocer, ingresando el dni de la misma
                otra_cuenta = self.find_by_dni(otra_cuenta_dni)
                return otra_cuenta
              
                                      
            except Exception as e:
                return("No se encontró la cuenta.")
        else:
            return("Acción no permitida para cuentas no administrativas.")
