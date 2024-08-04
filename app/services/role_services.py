from app.models import Role, Account
from app.repositories.role_repository import RoleRepository
from app.services.account_services import AccountService
from app.services.format_logs import formatLogs

logging = formatLogs('roletLogger')


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
            logging.info("Role saved")
            return self.repository.save(role)
        else:
            logging.warning("You do not have permission to add a role")
            return ("No tiene permiso para realizar esta acción")
        
    # Sólo puede eliminar roles un usuario SUadmin
    def delete(self, role_id: int, admin_id: int) -> None:
        acc_srv = 0
        if admin_id != 0:
            acc_srv = self.acc_srvc.find_by_id(admin_id)

        if (isinstance(acc_srv, Account) and acc_srv.id_role == 1) or acc_srv == 0:
            role = self.repository.find_by_id(role_id)
            if isinstance(role, Role):
                logging.info("Role deleted")
                return self.repository.delete(role)        
        else:
            logging.warning("You do not have permission to remove a role")
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
                logging.info("Role updated")
                return self.repository.update(role)
            else:
                logging.warning("there is no role to update")
                return ("No existe el rol")
        else:
            logging.warning("You do not have permission to update role")
            return ("No tiene permiso para realizar esta acción")
        
    def find_by_id(self, id: int) -> Role:
        if id is None or id == 0:
            return None
        res = self.repository.find_by_id(id)
        if res != None:
            logging.info("Role found by id")
            return res
        else:
              logging.warning("Role not found by id")
              return "Role not found - 404"
    
    def find_by_role_name(self, role_name: str):
        res = self.repository.find_by_role_name(role_name.capitalize())
        if res != None:
            logging.info("Role found by name")
            return res
        else:
            logging.warning("Role not found by name")
            return "Role not found - 404"
        
    def get_all_roles(self):
        logging.info ("information Role found")
        return self.repository.get_all()