from dataclasses import dataclass
from app import db
@dataclass
class Account( db.Model ):
    __tablename__ = 'accounts'
    id_account = db.Column('id_account',db.Integer, primary_key=True, autoincrement= True)
    username = db.Column('username', db.String(45), unique=True, nullable=False) 
    password = db.Column('password', db.String, nullable=False)
    email = db.Column('email', db.String(100), unique=True, nullable=False) 
    first_name =  db.Column('first_name', db.String(45), nullable=False)
    last_name =  db.Column('last_name', db.String(45), nullable=False)
    phone = db.Column('phone', db.String(45), unique=True, nullable=False)
    address = db.Column ('address', db.String(45), nullable=False)
    dni = db.Column ('dni', db.Integer(), unique=True, nullable=False)
    birthdate = db.Column('birthdate', db.DateTime, nullable=False)
    is_admin = db.Column('is_admin', db.Boolean, nullable=False, default = False)
    # Relación one-to-many: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    # One account - many wallets
    wallets = db.relationship("Wallet", back_populates="accounts", cascade="all, delete-orphan")
    

    """ def add_role(self, wallet):
        if wallet not in self.wallets:
            self.wallets.append(wallet)
    
    def remove_role(self, wallet):
        if wallet in self.wallets:
            self.wallets.remove(wallet) """