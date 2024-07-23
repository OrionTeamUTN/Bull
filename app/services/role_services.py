from app.models import Role, Account
from app.repositories.role_repository import RoleRepository
from app.services.account_services import AccountService

class RoleServices:
   
    def __init__(self):
        self.repository = RoleRepository()
        self.acc_srvc = AccountService()
        
    # Sólo puede agregar roles un usuario SUadmin
    def save(self, args: dict, admin_id: int) -> Role:
        acc_srv = 0
        # Modificación para poder crear roles
        if admin_id != 0:
            acc_srv = self.acc_srvc.find_by_id(admin_id)

        if (isinstance(acc_srv, Account) and acc_srv.id_role == 1) or acc_srv == 0:
            role = Role()
            for key, value in args.items():
                setattr(role, key, value) if hasattr (role, key) else print("Atributo desconocido")
            role.role_name = role.role_name.capitalize()
            return self.repository.save(role)
        else:
            return ("No tiene permiso para realizar esta acción")
        
    # Sólo puede eliminar roles un usuario SUadmin
    def delete(self, role_id: int, admin_id: int) -> None:
        acc_srv = 0
        if admin_id != 0:
            acc_srv = self.acc_srvc.find_by_id(admin_id)

        if (isinstance(acc_srv, Account) and acc_srv.id_role == 1) or acc_srv == 0:
            role = self.repository.find_by_id(role_id)
            if isinstance(role, Role):
                return self.repository.delete(role)        
        else:
            return ("No tiene permiso para realizar esta acción")
        
    # Sólo puede modificar roles un usuario SUadmin
    def update(self, role_id: int, new_role: dict, admin_id: int) -> Role:

        acc_srv = 0
        if admin_id != 0:
            acc_srv = self.acc_srvc.find_by_id(admin_id)

        if acc_srv == 0 or (isinstance(acc_srv, Account) and acc_srv.id_role == 1):
            role = self.repository.find_by_id(role_id)
            if isinstance(role, Role):
                role.role_name = new_role['role_name'].capitalize()
                return self.repository.update(role)
            else:
                return ("No existe el rol")
        else:
            return ("No tiene permiso para realizar esta acción")
        
    def find_by_id(self, id: int) -> Role:
        if id is None or id == 0:
            return None
        res = self.repository.find_by_id(id)
        if res != None:
            return res
        else:
              return "Role not found - 404"
    
    def find_by_role_name(self, role_name: str):
        res = self.repository.find_by_role_name(role_name.capitalize())
        if res != None:
            return res
        else:
            return "Role not found - 404"
        
    def get_all_roles(self):
        return self.repository.get_all()