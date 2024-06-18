from dataclasses import dataclass
from app import db
@dataclass(init=False)
class Wallet(db.Model):
    __tablename__ = 'wallets'
    id_wallet = db.Column('id_wallet',db.Integer, primary_key=True, autoincrement= True)
    balance =  db.Column('balance', db.Integer, nullable=False, default=0)
    id_owner_account = db.Column('id_account', db.ForeignKey('accounts.id_account'), nullable=False)
    accounts = db.relationship('Account', uselist=False, back_populates='wallets')
    id_wallet_coin = db.Column('id_coin', db.ForeignKey('coins.id_coin'), nullable=False)
    coin = db.relationship('Coin', back_populates='wallet')
    