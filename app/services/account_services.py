from app.models import Account
from app.repositories.account_repository import Accounrepository
from app.services.security import SecurityManager, WerkzeugSecurity

repository = Accounrepository()
class accountservice:
    
    #Clase encargada de crear el CRUD. 
    
    def __init__(self) -> None:
        self.__security = SecurityManager(WerkzeugSecurity())

    def save(self, user: Account) -> Account:
        user.password = self.__security.generate_password(user.password)
        return repository.save(user)
    

    def update(self, user: Account, id: int) -> Account:
        return repository.update(user, id)
    
    def delete(self, user: Account) -> None:
        repository.delete(user)
    

    def find(self, id: int) -> Account:
        return repository.find(id)
    
    def find_by_username(self, username: str):
        return repository.find_by_username(username)
    
    def find_by_dni(self, dni: int):
        return repository.find_by_dni(dni)
    
    
    def check_auth(self, dni, password) -> bool:
        user = self.find_by_dni(dni)
        if user is not None:
            return self.__security.check_password(user.password, password)
        else:
            return False
    
    
    def get_other_account_info (self, otra_cuenta_dni:int, admin_dni:int):
        return repository.get_other_account_info(otra_cuenta_dni, admin_dni)
    