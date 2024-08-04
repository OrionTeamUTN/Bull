from app.models import Account
from app.repositories.account_repository import AccounRepository
from app.services.format_logs import formatLogs
from app.services.security import SecurityManager, WerkzeugSecurity

logging = formatLogs('accountLogger')

class AccountService:
    
    #Clase encargada de crear el CRUD. 
    
    def __init__(self) -> None:
        self.__security = SecurityManager(WerkzeugSecurity())
        self.repository = AccounRepository()

    def save(self, args: dict):
        account = Account()
        for key, value in args.items():
            setattr(account, key, value) if hasattr (account, key) else print("Atributo desconocido cuando se registra")
        account.email = account.email.lower()
        account.username = account.username.lower()
        account.first_name = account.first_name.capitalize()
        account.last_name = account.last_name.capitalize()
        account.password = self.__security.generate_password(args['password'])
        logging.info("The account was saved successfully")
        return self.repository.save(account)
    
    def update(self, account: dict, id: int) -> Account:
        entity = self.find_by_id(id)
        if isinstance(entity, Account):
            for key, value in account.items():
                setattr(entity, key, value)
            entity.username.lower()
            entity.email.lower()
            entity.first_name.capitalize()
            entity.last_name.capitalize()
            entity.password = self.__security.generate_password(account['password'])
            logging.info("Account update")
        else:
            logging.warning("Account not found to update")
            return "No existe la cuenta"
        
        return self.repository.update(entity)
    
    def delete(self, id: int) -> str:
        try:
            res = self.find_by_id(id)
            if res is not None:
                self.repository.delete(res)
                logging.info("Account deleted successfully")
                return "Deleted"
            else:
                logging.warning("Account not found to delete")
                return "Account not found, not deleted"
        except:
            logging.error("Error to try delete")
            return "Error to try delete"
    

    def find_by_id(self, id: int) -> Account:
        if id is None or id == 0:
            logging.warning("Id no encontradoAccount not found by id")
            return None
        res = self.repository.find_by_id(id)
        if res != None:
            logging.info("Account found by id")
            return res
        else:
            logging.warning("Account not found by id")
            return "Account not found - 404"
    
    def find_by_username(self, username: str):
        res = self.repository.find_by_username(username)
        if res != None:
            logging.info("Account found by username")
            return res
        else:
            logging.warning("Account not found by username")
            return "Account not found - 404"
    
    def find_by_dni(self, dni: int):
        res = self.repository.find_by_dni(dni)
        if res != None:
            logging.info("Account found by dni")
            return res
        else:
            logging.warning("Account not found by dni")
            return "No se encontró la cuenta."
    
    def check_auth(self, dni, password) -> bool:
        user = self.find_by_dni(dni)
        if user is not None:
            passw= self.__security.check_password(user.password, password)
            logging.info("Correct password")
            return passw
        else:
            logging.warning("Incorrect password")
            return False
    

    def get_other_account_info (self, otra_cuenta_dni:int, admin_dni:int):
        #metodo encargado de verificar si el usuario que pide la cuenta es admin
        #para poder utilizar este metodo el admin debe ingresar su dni tambien, para verificar que es admin 
        admin_account = self.find_by_dni(admin_dni)
        if admin_account and admin_account.id_role == 1 or admin_account.id_role == 2 :
            #si es admin, traera la informacion de la cuenta que el admin desee conocer, ingresando el dni de la misma
            otra_cuenta = self.find_by_dni(otra_cuenta_dni)
            logging.info("Information from another account obtained")
            return otra_cuenta
        else:
            logging.warning("Action not allowed for non-administrative accounts to obtain information")
            return("Acción no permitida para cuentas no administrativas.")
        