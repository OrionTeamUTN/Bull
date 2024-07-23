from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Role(db.Model):
    __tablename__ = 'roles'
    id_role = db.Column('id_role', db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column('role_name', db.String(25), unique=True, nullable=False)
    # Relación one-to-many: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    # One role - many accounts
    accounts_role = db.relationship("Account", back_populates="roles", cascade="all, delete-orphan")