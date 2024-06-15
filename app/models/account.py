from dataclasses import dataclass
from app import db
@dataclass
class Account( db.Model ):
    __tablename__ = 'accounts'
    id_account = db.Column('id_account',db.Integer, primary_key=True, autoincrement= True)
    username = db.Column('username', db.String(45), nullable=False)
    password = db.Column('password', db.String, nullable=False)
    email = db.Column('email', db.String(100), nullable=False)
    is_admin = db.Column('is_admin', db.Boolean, nullable=False, default = False)
    surname =  db.Column('surname', db.String(45), nullable=False)
    phone = db.Column('phone', db.String(45), nullable=False)
    address = db.Column ('address', db.String(45), nullable=False)
    dni = db.Column ('dni', db.Integer(), nullable=False)
    birthdate = db.Column('birthdate', db.DateTime, nullable=False)
    wallets = db.relationship("Wallet", back_populates="accounts", uselist=False)
    

    def add_role(self, wallet):
        if wallet not in self.wallets:
            self.wallets.append(wallet)
    
    def remove_role(self, wallet):
        if wallet in self.wallets:
            self.wallets.remove(wallet)