from app.models import Role
from app import db
from sqlalchemy.exc import IntegrityError, NoResultFound

class RoleRepository:

    def save(self, role: Role) -> Role:
        try:
            db.session.add(role) 
            db.session.commit()
            return role
        except IntegrityError:
            db.session.rollback()
            return None
    
    def update(self, role: Role) -> Role:
        try:
            db.session.add(role)
            db.session.commit()
            return role
        except IntegrityError:
            db.session.rollback()
            return None
    
    def delete(self, role: Role) -> None:
        try:
            db.session.delete(role)
            db.session.commit()
            return "Deleted"
        except IntegrityError:
            db.session.rollback()
            print("Rollback en repository")
            return None

    def find_by_id(self, id: int) -> Role :
        try:
            return db.session.query(Role).filter(Role.id_role == id).one()
        except NoResultFound:
            return None

    def find_by_role_name(self, role_name: str):
        try:
            return db.session.query(Role).filter(Role.role_name == role_name).one_or_none()
        except NoResultFound:
            return None

    def get_all(self) -> list[Role]:
        return db.session.query(Role).all()